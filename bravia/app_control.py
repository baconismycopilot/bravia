"""
app_control
~~~~~~~~~~~

Module for the appControl service.
"""

from typing import List

from .bravia import Bravia


class AppControl(Bravia):
    """
    Provides methods to interact with the appControl
    service.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = "appControl"

    @property
    def app_list(self) -> List[dict]:
        """
        Get a list of applications available on the TV.

        :rtype: List[dict]
        """

        params = {
            "method": "getApplicationList",
            "version": "1.0",
            "id": self._rand_id(),
            "params": [],
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    @property
    def app_status(self) -> List[dict]:
        """
        Get the status of service(s). Defaults to all.

        :rtype: List[dict]
        """

        params = {
            "method": "getApplicationStatusList",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def set_active_app(self, app_uri: str) -> List[dict]:
        """
        Start a service that is in self.app_list().

        :param app_uri: App URI
        :type app_uri: :class:`str`

        :rtype: List[dict]
        """

        params = {
            "method": "setActiveApp",
            "id": self._rand_id(),
            "params": [{"uri": app_uri}],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def terminate_apps(self) -> List[dict]:
        """
        Terminate all terminable apps. This is terminal.

        :rtype: List[dict]
        """

        params = {
            "method": "terminateApps",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp
