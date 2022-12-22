"""
The base class for bravia.

The bravia project was written and tested against
the XBR-65X900H model.
"""

from random import randint
from typing import List, Optional

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
    :type pre_shared_key: :class:`Optional[str]`

    `Sony Developer Docs <https://pro-bravia.sony.net/develop/integrate/ip-control/index.html>`_

    Usage:

    >>> from bravia import Bravia
    >>> b = Bravia(ip='192.168.1.25')
    >>> b.api_info()
    """

    def __init__(self, ip: str, pre_shared_key: Optional[str]):
        self.base_url = f"http://{ip}/sony"
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

    def build_params(
        self, method: str, version: Optional[str] = "1.0", params: Optional[list] = []
    ) -> dict:
        """
        Build request parameters.

        :param method: Name of the method
        :type method: :class:`str`
        :param params: Optionally provided params, defaults to :class:`[]`
        :type params: :class:`Optional[list]`
        :param version: Version of the method to use, defaults to 1.0
        :type version: :class`dict`

        :return: Dictionary of request parameters
        :rtype: :class:`dict`
        """

        body = {
            "method": method,
            "id": self._rand_id(),
            "params": params,
            "version": version,
        }

        return body

    def api_info(self, service=None) -> List[dict]:
        """
        Get the available services and their
        API methods.

        :param service: Service name, defaults to all
        :type service: :class:`str`

        :rtype: List[dict]
        """

        if not service:
            services = [
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
            services = [{"services": [service]}]

        prepared_params = self.build_params(
            method="getSupportedApiInfo", params=services, version="1.0"
        )
        resp = self._get(params=prepared_params, service="guide")

        return resp

    @staticmethod
    def _rand_id() -> int:
        """
        The Bravia TV API uses a customized JSON RPC
        protocol, which reserves the 'id' value 0. We
        start with 1.

        :return: Random integer in designated range
        :rtype: int
        """

        rand_min: int = 1
        rand_max: int = 2147483647
        tx_id: int = randint(rand_min, rand_max)

        return tx_id

    @property
    def wol_mode(self) -> dict:
        """
        Get the Wake on LAN mode.

        :rtype: dict
        """

        prepared_params = self.build_params(method="getWolMode")
        resp = self._get(params=prepared_params, service="system")

        return resp

    def set_wol_mode(self, mode: bool) -> dict:
        """
        Set the Wake on LAN mode.

        :param mode: True or False
        :type mode: :class:`bool`

        :rtype: dict
        """

        prepared_params = self.build_params(
            method="setWolMode", params=[{"enabled": mode}]
        )
        resp = self._set(params=prepared_params, service="system")

        return resp

    @property
    def system_info(self) -> List[dict]:
        """
        Get system information.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="getSystemInformation")
        resp: Response = self._get(params=prepared_params, service="system")

        return resp

    @property
    def network_settings(self) -> List[dict]:
        """
        Get network information.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(
            method="getNetworkSettings", params=[{"netif": ""}]
        )
        resp: Response = self._get(params=prepared_params, service="system")

        return resp

    @property
    def interface_information(self) -> List[dict]:
        """
        Get inerface information.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="getInterfaceInformation")
        resp: Response = self._get(params=prepared_params, service="system")

        return resp

    @property
    def power_status(self) -> List[dict]:
        """
        Get the power status of the TV.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="getPowerStatus")
        resp: List[dict] = self._get(params=prepared_params, service="system")

        return resp

    @property
    def supported_functions(self) -> List[dict]:
        """
        Get the supported functions of the device.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="getSystemSupportedFunction")
        resp: List[dict] = self._get(params=prepared_params, service="system")

        return resp

    def power_on(self) -> list:
        """
        Power on the TV.

        :rtype: list
        """

        prepared_params = self.build_params(
            method="setPowerStatus",
            params=[{"status": True}],
        )
        resp: List[dict] = self._set(params=prepared_params, service="system")

        return resp

    def power_off(self) -> list:
        """
        Power on the TV.

        :rtype: list
        """

        prepared_params = self.build_params(
            method="setPowerStatus",
            params=[{"status": False}],
        )
        resp: List[dict] = self._set(params=prepared_params, service="system")

        return resp

    @property
    def power_saving_mode(self) -> dict:
        """
        Get the power saving mode.

        :rtype: dict
        """

        prepared_params = self.build_params(method="getPowerSavingMode")
        resp: List[dict] = self._get(params=prepared_params, service="system")

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

        prepared_params = self.build_params(
            method="setPowerSavingMode",
            params=[{"mode": mode}],
        )
        resp: List[dict] = self._get(params=prepared_params, service="system")

        return resp

    @property
    def led_status(self) -> List[dict]:
        """
        Get the LED indicator status.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="getLEDIndicatorStatus")
        resp: List[dict] = self._get(params=prepared_params, service="system")

        return resp

    def set_led_status(self, mode: str, status: bool) -> dict:
        """
        Set the LED indicator mode.

        Options for :class:`mode`:

        - Demo
        - AutoBrightnessAdjust
        - Dark
        - SimpleResponse
        - Off

        :param mode: LED mode
        :type mode: :class:`str`
        :param status: True or False.
        :type status: :class:`bool`

        :rtype: dict
        """

        if self.led_status == mode and self.led_status.status is True:
            return {"msg": f"LED already set to {mode}."}

        prepared_params = self.build_params(
            method="setLEDIndicatorStatus",
            params=[{"mode": mode, "status": status}],
            version="1.1",
        )
        resp: List[dict] = self._set(params=prepared_params, service="system")

        return resp

    def set_language(self, lang: str = "eng") -> dict:
        """
        Set the language of the TV. This setting
        is region specific.

        :param lang: Set the language, defaults to :class:`eng`
        :type lang: :class:`str`

        :rtype: dict
        """

        prepared_params = self.build_params(
            method="setLanguage",
            params=[{"language": lang}],
        )
        resp: List[dict] = self._set(params=prepared_params, service="system")

        return resp

    def reboot(self):
        """
        Reboot the TV.

        :rtype: list
        """

        prepared_params = self.build_params(method="requestReboot")
        resp: List[dict] = self._set(params=prepared_params, service="system")

        return resp
