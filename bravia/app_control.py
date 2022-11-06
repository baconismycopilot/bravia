"""
app_control
-----------

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

    def app_list(self) -> List[dict]:
        """
        Get a list of applications available on the TV.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getApplicationList",
            "version": "1.0",
            "id": self._rand_id(),
            "params": []
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def get_app_status(self, app=None) -> List[dict]:
        """
        Get the status of service(s). If service is not
        specified then all apps will be returned.

        :param app: :class:`Optional[str]` Name of service to query.

        :return: :class:`List[dict]`
        """

        if app is None:
            app_params = [f"{app}"]
        else:
            app_params = []

        params = {
            "method": "getApplicationStatusList",
            "id": self._rand_id(),
            "params": app_params,
            "version": "1.0"
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def set_active_app(self, app_uri: str) -> List[dict]:
        """
        Start a service that is in self.app_list().

        :param str app_uri: App URI

        :return: :class:`List[dict]`
        """

        params = {
            "method": "setActiveApp",
            "id": self._rand_id(),
            "params": [{
                "uri": app_uri
            }],
            "version": "1.0"
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def terminate_apps(self) -> List[dict]:
        """
        Terminate all terminable apps. This is terminal.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "terminateApps",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp
