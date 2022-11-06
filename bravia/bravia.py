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


def handle_error(resp: Response) -> List[dict]:
    """
    Helper to check for and return the error
    if it exists in the response.

    :param resp:
    :return: List[dict
    """

    if resp.json().get("error"):
        return resp.json()

    return resp.json().get("result")


class Bravia:
    """
    Base class containing methods to interact
    with the Bravia line of TVs.

    :param ip: :class:`str` IP address of the device.

    `Sony Developer Docs <https://pro-bravia.sony.net/develop/integrate/ip-control/index.html>`_

    Usage:

    >>> from bravia import Bravia
    >>> b = Bravia(ip='192.168.1.25')
    >>> b.api_info()
    """

    def __init__(self, ip: str, service: str = "system"):
        self.base_url = f"http://{ip}/sony"
        self.service = "system" if None else service

    def _get(self, params: dict, service: str) -> List[dict]:
        """
        Get data for the specified service and method.

        :param params: :class:`dict`
        :param service: :class:`str`

        :return: :class:`List[dict]`
        """

        url = f"{self.base_url}/{service}"
        headers = {"X-Auth-PSK": "meseeks"}
        resp: Response = requests.post(url, json=params, headers=headers)

        return handle_error(resp)

    def _set(self, params: dict, service: str) -> List[dict]:
        """
        Set parameters for the given service and method.

        :param params: :class:`dict`
        :param service: :class:`str`

        :return: :class:`Response <Response>` object
        """

        url = f"{self.base_url}/{service}"
        headers = {"X-Auth-PSK": "meseeks"}
        resp: Response = requests.post(url, json=params, headers=headers)

        return handle_error(resp)

    def api_info(self, service=None) -> List[dict]:
        """
        Get the available services and their
        API methods.

        If service is not specified then all
        services are returned.

        :param service: :class:`Optional[str]`

        :return: :class:`List[dict]`
        """

        if service is None:
            svc_params = [
                {
                    "services": [
                        "appControl",
                        "audio",
                        "avContent",
                        "encryption",
                        "system",
                        "video",
                        "videoScreen",
                    ]
                }
            ]
        else:
            svc_params = [{"services": [service]}]

        params = {
            "method": "getSupportedApiInfo",
            "id": self._rand_id(),
            "params": svc_params,
            "version": "1.0",
        }

        app = "guide"
        resp = self._get(params=params, service=app)

        return resp

    def get_wol_mode(self) -> dict:
        """
        Get the Wake on LAN mode.

        :return: :class:`dict`
        """

        params = {
            "method": "getWolMode",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp = self._get(params=params, service=self.service)

        return resp

    def set_wol_mode(self, mode: str) -> dict:
        """
        Set the Wake on LAN mode.

        :param str mode: on or off
        :return: :class:`dict`
        """

        current_mode: str = self.get_wol_mode().get("enabled")

        if str(mode).lower() == "on":
            toggle = True
        else:
            toggle = False

        if current_mode == toggle:
            return {"msg": f"WoL mode was already {mode}."}

        params = {
            "method": "setWolMode",
            "id": self._rand_id(),
            "params": [{"enabled": toggle}],
            "version": "1.0",
        }

        resp = self._set(params=params, service=self.service)

        # TODO: Error logic in _get and _set methods.
        # if len(resp.json().get("result")) == 0:
        # return {"msg": f"WoL mode set to {mode}."}

        return resp

    def get_service_info(self, service: str) -> dict:
        """
        Get the available API methods for a service.

        :param service: :class:`str` Name of the service to get.

        :return: :class:`dict`
        """

        return self.api_info(service=service)

    @staticmethod
    def _rand_id() -> int:
        """
        The Bravia TV API uses a customized JSON RPC
        protocol, which reserves the 'id' value 0. We
        start with 1.

        :return :class:`int` Random integer
        """

        rand_min: int = 1
        rand_max: int = 2147483647
        tx_id: int = randint(rand_min, rand_max)

        return tx_id

    def get_system_information(self) -> List[dict]:
        """
        Get system information.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getSystemInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    def get_network_settings(self) -> List[dict]:
        """
        Get network information for all, interfaces.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getNetworkSettings",
            "id": self._rand_id(),
            "params": [{"netif": ""}],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    def get_interface_information(self) -> List[dict]:
        """
        Get information about the REST API provided
        by device server.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getInterfaceInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    def get_power_status(self) -> List[dict]:
        """
        Get the power status of the TV.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getPowerStatus",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service="system")

        return resp

    def get_power_saving_mode(self):
        """
        Get the power saving mode.

        :return: :class:`dict`
        """

        params = {
            "method": "getPowerSavingMode",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    def get_led_status(self) -> List[dict]:
        """
        Get the LED indicator status.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getLEDIndicatorStatus",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    def get_supported_functions(self) -> List[dict]:
        """
        Get the supported functions of the device.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getSystemSupportedFunction",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    def set_power_status(self, status: str) -> dict:
        """
        Turn the TV on or off.

        :param str status: `on` or `off`

        :return: :class:`dict`
        """

        current_status: str = self.get_power_status()[0].get("status")
        if current_status == "active":
            current_status: bool = True
        else:
            current_status: bool = False

        if str(status).lower() == "on":
            toggle = True
        else:
            toggle = False

        if current_status == toggle:
            return {"msg": f"Power status was already {status}."}

        params = {
            "method": "setPowerStatus",
            "id": self._rand_id(),
            "params": [{"status": toggle}],
            "version": "1.0",
        }

        resp: List[dict] = self._set(params=params, service="system")

        return resp

    def set_power_saving_mode(self, mode: str):
        """
        Set the power saving mode.

        Available options:

        * off
        * low
        * high
        * pictureOff

        :return: :class:`dict`
        """

        if self.get_power_saving_mode() == mode:
            return {"msg": f"Power saving mode already set to {mode}."}

        params = {
            "method": "setPowerSavingMode",
            "id": self._rand_id(),
            "params": [{"mode": mode}],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)
        # if len(resp.json().get("result")) == 0:
        # return {"msg": f"Power saving mode set to {mode}."}

        return resp

    def set_led_status(self, mode: str, status: str) -> dict:
        """
        Set the LED indicator mode.

        Available options:

        * Demo
        * AutoBrightnessAdjust
        * Dark
        * SimpleResponse
        * Off

        :return: :class:`dict`
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
            "id": self._rand_id(),
            "params": [{"mode": mode, "status": toggle}],
            "version": "1.1",
        }

        resp: Response = self._set(params=params, service=self.service)

        # if len(resp.json().get("result")) == 0:
        # return {"msg": f"LED set to {mode}."}

        return resp

    def set_language(self, lang: str) -> dict:
        """
        Set the language of the TV. This setting
        is region specific.

        :param lang: :class:`str`

        :return: :class:`dict`
        """

        params = {
            "method": "setLanguage",
            "id": self._rand_id(),
            "params": [{"language": lang}],
            "version": "1.0",
        }

        resp: Response = self._set(params=params, service=self.service)

        return resp

    def reboot(self):
        """
        Reboot the TV.

        :return: :class:`[]`
        """

        params = {
            "method": "requestReboot",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._set(params=params, service=self.service)

        return resp
