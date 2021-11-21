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

from bravia.models import (
    SystemInfo,
    NetworkInfo,
    PowerStatus,
    InterfaceInfo,
    LEDIndicator,
    SupportedFunc,
)


class Bravia:
    """
    Base class containing methods to interact
    with the Bravia line of TVs.

    `Sony Developer Docs <https://pro-bravia.sony.net/develop/integrate/ip-control/index.html>`_
    """

    def __init__(self, protocol: str, ip: str, base: str):
        self.base_url = f"{protocol}://{ip}{base}"
        self.app = "system"

    def api_info(self, service=None) -> dict:
        """
        Get the available services and their
        API methods.

        If service is not specified then all
        services are returned.

        :param [Optional] service:

        :return: :class:`dict` response
        :rtype: :class:`dict`
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
            "id": self.rand_id(),
            "params": svc_params,
            "version": "1.0"
        }

        app = "guide"
        resp = self._get(params=params, app=app)

        if resp.json().get("error"):
            return resp.json()

        return resp.json().get("result")[0]

    def get_wol_mode(self) -> dict:
        """
        Get the Wake on LAN mode.

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "getWolMode",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp = self._get(params=params, app=self.app)
        data: dict = resp.json()["result"][0]

        return data

    def set_wol_mode(self, mode: str):
        """
        Set the Wake on LAN mode.

        :param str mode: on or off
        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        current_mode: str = self.get_wol_mode().get("enabled")

        if str(mode).lower() == "on":
            toggle = True
        else:
            toggle = False

        if current_mode == toggle:
            return {'msg': f"WoL mode was already {mode}."}

        params = {
            "method": "setWolMode",
            "id": self.rand_id(),
            "params": [{"enabled": toggle}],
            "version": "1.0"
        }

        resp = self._set(params=params, app=self.app)

        if len(resp.json().get("result")) == 0:
            return {"msg": f"WoL mode set to {mode}."}

        data: dict = resp.json()

        return data

    def get_service_info(self, service: str) -> dict:
        """
        Get the available API methods for a service.

        :param str service:
        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        return self.api_info(service=service)

    @staticmethod
    def rand_id() -> int:
        """
        The Bravia TV API uses a customized version of the JSON RPC
        protocol, which reserves the 'id' value 0. We
        start with 1 and it must be int.

        :return :class:`int` random integer
        :rtype: :class:`int`
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

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
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

        :return: :class:`Response <Response>` object
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

    def get_system_information(self) -> SystemInfo:
        """
        Get system information.

        :return: :class:`SystemInfo <SystemInfo>` object
        :rtype: bravia.models.SystemInfo
        """

        params = {
            "method": "getSystemInformation",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: SystemInfo = SystemInfo(**resp.json().get("result")[0])

        return data

    def get_network_settings(self) -> dict:
        """
        Get network information for all, interfaces.

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "getNetworkSettings",
            "id": self.rand_id(),
            "params": [{"netif": ""}],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: NetworkInfo = NetworkInfo(**resp.json().get("result")[0][0])

        return data.dict()

    def get_interface_information(self) -> InterfaceInfo:
        """
        Get information about the REST API provided
        by device server.

        :return: :class:`InterfaceInfo <InterfaceInfo>` object
        :rtype: bravia.models.InterfaceInfo
        """

        params = {
            "method": "getInterfaceInformation",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: InterfaceInfo = InterfaceInfo(**resp.json().get("result")[0])

        return data

    def get_power_status(self) -> PowerStatus:
        """
        Get the power status of the TV.

        :return: :class:`PowerStatus <PowerStatus>` object
        :rtype: bravia.models.PowerStatus
        """

        params = {
            "method": "getPowerStatus",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: PowerStatus = PowerStatus(**resp.json().get("result")[0])

        return data

    def get_power_saving_mode(self):
        """
        Get the power saving mode.

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "getPowerSavingMode",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: dict = resp.json().get("result")[0]

        return data

    def get_led_status(self) -> LEDIndicator:
        """
        Get the LED indicator status.

        :return: :class:`LEDIndicator <LEDIndicator>` object
        :rtype: bravia.models.LEDIndicator
        """

        params = {
            "method": "getLEDIndicatorStatus",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: LEDIndicator = LEDIndicator(**resp.json().get("result")[0])

        return data

    def get_supported_functions(self) -> List[SupportedFunc]:
        """
        Get the supported functions of the device.

        :return: :class:`List[SupportedFunc] <SupportedFunc>` object
        :rtype: List[bravia.models.SupportedFunc]
        """

        params = {
            "method": "getSystemSupportedFunction",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: List[SupportedFunc] = [
            SupportedFunc(**x) for x in resp.json()['result'][0]
        ]

        return data

    def set_power_status(self, status: str) -> dict:
        """
        Turn the TV on or off.

        :param str status: `on` or `off`

        :return: :class:`dict`
        :rtype: :class:`dict`
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

        params = {
            "method": "setPowerStatus",
            "id": self.rand_id(),
            "params": [{"status": toggle}],
            "version": "1.0"
        }

        resp: Response = self._set(params=params, app=self.app)
        data: dict = resp.json()

        return data

    def set_power_saving_mode(self, mode: str):
        """
        Set the power saving mode.

        Available options:

        * off
        * low
        * high
        * pictureOff


        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        if self.get_power_saving_mode() == mode:
            return {"msg": f"Power saving mode already set to {mode}."}

        params = {
            "method": "setPowerSavingMode",
            "id": self.rand_id(),
            "params": [{"mode": mode}],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        if len(resp.json().get("result")) == 0:
            return {"msg": f"Power saving mode set to {mode}."}

        data: dict = resp.json().get("result")

        return data

    def set_led_status(self, mode: str, status: str) -> dict:
        """
        Set the LED indicator mode.

        Available options:

        * Demo
        * AutoBrightnessAdjust
        * Dark
        * SimpleResponse
        * Off

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        led_status: LEDIndicator = self.get_led_status()
        if led_status.mode == mode and led_status.status is True:
            return {"msg": f"LED already set to {mode}."}

        if status.lower() == "on":
            toggle: str = "true"
        else:
            toggle: str = "false"

        params = {
            "method": "setLEDIndicatorStatus",
            "id": self.rand_id(),
            "params": [{
                "mode": mode,
                "status": toggle
            }],
            "version": "1.1"
        }

        resp: Response = self._set(params=params, app=self.app)

        if len(resp.json().get("result")) == 0:
            return {"msg": f"LED set to {mode}."}

        data: dict = resp.json()

        return data

    def set_language(self, lang: str) -> dict:
        """
        Set the language of the TV. This setting
        is region specific.

        :param str lang:

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "setLanguage",
            "id": self.rand_id(),
            "params": [{"language": lang}],
            "version": "1.0"
        }

        resp: Response = self._set(params=params, app=self.app)
        data: dict = resp.json()

        return data

    def reboot(self):
        """
        Reboot the TV.

        :return:
        """

        params = {
            "method": "requestReboot",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._set(params=params, app=self.app)
        data: dict = resp.json()

        return data
