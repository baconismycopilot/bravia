"""
The base class for bravia.

The bravia project was written and tested against
the XBR-65X900H model.
"""

from random import randint
from typing import List

import requests
from requests import Response

from .utils import handle_error


class Bravia:
    """
    Base class containing methods to interact
    with the Bravia line of TVs.

    :param ip: IP address of the device
    :type ip: :class:`str`
    :param pre_shared_key: Pre-shared key configured on TV
    :type ip: :class:`Optional[str]`

    `Sony Developer Docs <https://pro-bravia.sony.net/develop/integrate/ip-control/index.html>`_

    Usage:

    >>> from bravia import Bravia
    >>> b = Bravia(ip='192.168.1.25')
    >>> b.api_info()
    """

    def __init__(self, ip: str, service: str = "system", pre_shared_key=None):
        self.base_url = f"http://{ip}/sony"
        self.service = "system" if None else service
        self.pre_shared_key = pre_shared_key if pre_shared_key else None

    def _get(self, params: dict, service: str) -> List[dict]:
        """
        Get data for the specified service and method.

        :param params: Parameters for the request
        :type params: :class:`dict`
        :param service: Name of the service
        :type service: :class:`str`

        :rtype: List[dict]
        """

        url = f"{self.base_url}/{service}"
        headers = {}

        if self.pre_shared_key:
            headers = {"X-Auth-PSK": f"{self.pre_shared_key}"}

        resp: Response = requests.post(url, json=params, headers=headers)

        return handle_error(resp)

    def _set(self, params: dict, service: str) -> List[dict]:
        """
        Set parameters for the given service and method.

        :param params: Parameters for the request
        :type params: :class:`dict`
        :param service: Name of the service
        :type service: :class:`str`

        :rtype: List[dict]
        """

        url = f"{self.base_url}/{service}"
        headers = {}

        if self.pre_shared_key:
            headers = {"X-Auth-PSK": f"{self.pre_shared_key}"}

        resp: Response = requests.post(url, json=params, headers=headers)

        return handle_error(resp)

    def api_info(self, service=None) -> List[dict]:
        """
        Get the available services and their
        API methods.

        :param service: Service name, defaults to all
        :type service: :class:`Optional[str]`

        :rtype: List[dict]
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

    def _wol_mode(self) -> dict:
        """
        Get the Wake on LAN mode.

        :rtype: dict
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

        :param mode: One of Off
        :type mode: :class:`str`

        :rtype: dict
        """

        current_mode: str = self.wol_mode().get("enabled")

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

        return resp

    def get_service_info(self, service: str) -> dict:
        """
        Get the available API methods for a service.

        :param service: Name of the service to get
        :type service: :class:`str`

        :rtype: dict
        """

        return self.api_info(service=service)

    @staticmethod
    def _rand_id() -> int:
        """
        The Bravia TV API uses a customized JSON RPC
        protocol, which reserves the 'id' value 0. We
        start with 1.

        :return: Random integer in designated range.
        :rtype: int
        """

        rand_min: int = 1
        rand_max: int = 2147483647
        tx_id: int = randint(rand_min, rand_max)

        return tx_id

    @property
    def wol_mode(self):
        return self._wol_mode()

    @property
    def system_info(self) -> List[dict]:
        """
        Get system information.

        :rtype: List[dict]
        """

        params = {
            "method": "getSystemInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    @property
    def network_settings(self) -> List[dict]:
        """
        Get network information.

        :rtype: List[dict]
        """

        params = {
            "method": "getNetworkSettings",
            "id": self._rand_id(),
            "params": [{"netif": ""}],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    @property
    def interface_information(self) -> List[dict]:
        """
        Get inerface information.

        :rtype: List[dict]
        """

        params = {
            "method": "getInterfaceInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp

    @property
    def power_status(self) -> List[dict]:
        """
        Get the power status of the TV.

        :rtype: List[dict]
        """

        params = {
            "method": "getPowerStatus",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service="system")

        return resp

    @property
    def power_saving_mode(self) -> dict:
        """
        Get the power saving mode.

        :rtype: dict
        """

        params = {
            "method": "getPowerSavingMode",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    @property
    def led_status(self) -> List[dict]:
        """
        Get the LED indicator status.

        :rtype: List[dict]
        """

        params = {
            "method": "getLEDIndicatorStatus",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    @property
    def supported_functions(self) -> List[dict]:
        """
        Get the supported functions of the device.

        :rtype: List[dict]
        """

        params = {
            "method": "getSystemSupportedFunction",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def power_on(self) -> list:
        """
        Power on the TV.

        :rtype: list
        """

        params = {
            "method": "setPowerStatus",
            "id": self._rand_id(),
            "params": [{"status": True}],
            "version": "1.0",
        }

        resp: List[dict] = self._set(params=params, service="system")

        return resp

    def power_off(self) -> list:
        """
        Power on the TV.

        :rtype:
        """

        params = {
            "method": "setPowerStatus",
            "id": self._rand_id(),
            "params": [{"status": False}],
            "version": "1.0",
        }

        resp: List[dict] = self._set(params=params, service="system")

        return resp

    def set_power_saving_mode(self, mode: str) -> List[dict]:
        """
        Set the power saving mode.

        Available options:

        * off
        * low
        * high
        * pictureOff

        :param mode: Power saving mode
        :type mode: :class:`str`

        :rtype: dict
        """

        if self.power_saving_mode == mode:
            return {"msg": f"Power saving mode already set to {mode}."}

        params = {
            "method": "setPowerSavingMode",
            "id": self._rand_id(),
            "params": [{"mode": mode}],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

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

        :param mode: LED mode
        :type mode: :class:`str`
        :param status: One or off.
        :type status: :class:`str`

        :rtype: dict
        """

        led_status: LEDIndicator = self.led_status()
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

        resp: List[dict] = self._set(params=params, service=self.service)

        return resp

    def set_language(self, lang: str) -> dict:
        """
        Set the language of the TV. This setting
        is region specific.

        :param lang: Set the language
        :type lang: :class:`str`

        :rtype: dict
        """

        params = {
            "method": "setLanguage",
            "id": self._rand_id(),
            "params": [{"language": lang}],
            "version": "1.0",
        }

        resp: List[dict] = self._set(params=params, service=self.service)

        return resp

    def reboot(self):
        """
        Reboot the TV.

        :rtype: list
        """

        params = {
            "method": "requestReboot",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._set(params=params, service=self.service)

        return resp
