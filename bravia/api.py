"""
The base module for bravia. The api module
contains basic system level operations.

The bravia project was written and tested against
the XBR-65X900H model.
"""

from random import randint
from typing import List

import requests
from requests import Response

from .models import (
    NetworkInfoModel,
    SystemInfoModel,
    PowerStatusModel,
    InterfaceInfoModel,
    LEDIndicatorModel,
    SupportedFuncModel,
)


class BraviaBase:
    """
    Base class containing methods to interact
    with the Bravia line of TVs.

    https://pro-bravia.sony.net/develop/integrate/ip-control/index.html
    """

    def __init__(self, protocol: str, ip: str, base: str):
        self.base_url = f"{protocol}://{ip}{base}"

    def api_info(self, service=None) -> dict:
        """
        Get the available services and their
        API methods.

        If service is not specified then all
        services are returned.

        :param [Optional] service:

        :return: :class:`dict`
        """

        if service is None:
            svc_params = [{"services": [
                "appControl",
                "audio",
                "avContent",
                "encryption",
                "system",
                "video",
                "videoScreen",
            ]}]
        else:
            svc_params = [{"services": [service]}]

        params = {
            "method": "getSupportedApiInfo",
            "id": self._rand_id(),
            "params": svc_params,
            "version": "1.0"
        }
        app = "guide"
        resp = self._get(params=params, app=app)

        if resp.json().get("error"):
            return resp.json()

        return resp.json().get("result")[0]

    def get_service_info(self, service: str) -> dict:
        """
        Get the available API methods for a service.

        :param str service:
        :return: :class:`dict`
        :rtype: `dict`
        """

        return self.api_info(service=service)

    @staticmethod
    def _rand_id() -> int:
        """
        The Bravia TV API uses a customized version of the JSON RPC
        protocol, which reserves the 'id' value 0. We
        start with 1 and it must be int.

        :return :class:`int`
        """

        rand_min: int = 1
        rand_max: int = 2147483647
        tx_id: int = randint(rand_min, rand_max)

        return tx_id

    def _get(self, params: dict, app: str) -> Response:
        """
        Get data for the specified app and method.

        :param dict params:
        :param str app:

        :return :class:`Response <Response>` object
        """

        url = f"{self.base_url}/{app}"
        r: Response = requests.post(url, json=params)
        r.raise_for_status()

        return r

    def _set(self, params: dict, app: str) -> Response:
        """
        Set parameters for the given app and method.

        :param dict params:
        :param str app:

        :return :class:`Response <Response>` object
        """

        if not str(params.get("method")).startswith("set"):
            r: Response = Response()
            r.status_code = 404
            r.reason = f"Invalid method for {app}"

            return r

        url = f"{self.base_url}/{app}"
        r: Response = requests.post(url, json=params)
        r.raise_for_status()

        return r

    def get_system_information(self) -> SystemInfoModel:
        """
        Get system information.

        :return: :class:`SystemInfoModel <SystemInfoModel>` object
        :rtype: bravia.models.SystemInfoModel
        """

        app = "system"
        params = {
            "method": "getSystemInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=app)
        data: SystemInfoModel = SystemInfoModel(**resp.json().get("result")[0])

        return data

    def get_network_settings(self) -> dict:
        """
        Get network information for all, interfaces.

        :return: :class:`dict`
        :rtype: :class:`dict`
        """

        app = "system"
        params = {
            "method": "getNetworkSettings",
            "id": self._rand_id(),
            "params": [{"netif": ""}],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=app)
        data: NetworkInfoModel = NetworkInfoModel(**resp.json().get("result")[0][0])

        return data.dict()

    def get_interface_information(self) -> InterfaceInfoModel:
        """
        Get information about the REST API provided
        by device server.

        :return: :class:`InterfaceInfoModel <InterfaceInfoModel>` object
        :rtype: bravia.models.InterfaceInfoModel
        """

        app = "system"
        params = {
            "method": "getInterfaceInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=app)
        data: InterfaceInfoModel = InterfaceInfoModel(**resp.json().get("result")[0])

        return data

    def get_power_status(self) -> PowerStatusModel:
        """
        Get the power status of the TV.

        :return: :class:`PowerStatusModel <PowerStatusModel>` object
        :rtype: bravia.models.PowerStatusModel
        """

        app = "system"
        params = {
            "method": "getPowerStatus",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=app)
        data: PowerStatusModel = PowerStatusModel(**resp.json().get("result")[0])

        return data

    def get_led_status(self) -> LEDIndicatorModel:
        """
        Get the LED indicator status.

        :return: :class:`LEDIndicatorModel <LEDIndicatorModel>` object
        :rtype: bravia.models.LEDIndicatorModel
        """

        app = "system"
        params = {
            "method": "getLEDIndicatorStatus",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=app)
        data: LEDIndicatorModel = LEDIndicatorModel(**resp.json().get("result")[0])

        return data

    def get_supported_functions(self) -> List[SupportedFuncModel]:
        """
        Get the supported functions of the device.

        :return: :class:`List[LEDIndicatorModel] <LEDIndicatorModel>` object
        :rtype: List[bravia.models.LEDIndicatorModel]
        """

        app = "system"
        params = {
            "method": "getSystemSupportedFunction",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=app)
        data: List[SupportedFuncModel] = [
            SupportedFuncModel(**x) for x in resp.json()['result'][0]
        ]

        return data

    def set_power_status(self, status: str) -> dict:
        """
        Turn the TV on or off.

        :param str status: `on` or `off`

        :return: :class:`dict`
        :rtype: `dict`
        """

        current_status: str = self.get_power_status().status
        if current_status == "active":
            current_status: bool = True
        else:
            current_status: bool = False

        if str(status).lower() == "on":
            toggle = True
        else:
            toggle = False

        if current_status == toggle:
            return {'msg': f"Power status was already {status}."}

        app = "system"
        params = {
            "method": "setPowerStatus",
            "id": self._rand_id(),
            "params": [{"status": toggle}],
            "version": "1.0"
        }

        resp: Response = self._set(params=params, app=app)
        data: dict = resp.json()

        return data
