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

        prepared_params = self.build_params(method="getApplicationList")
        resp: List[dict] = self._get(params=prepared_params, service=self.service)

        return resp

    @property
    def app_status(self) -> List[dict]:
        """
        Get the status of service(s). Defaults to all.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="getApplicationStatusList")
        resp: List[dict] = self._get(params=prepared_params, service=self.service)

        return resp

    def set_active_app(self, app_uri: str) -> List[dict]:
        """
        Start a service that is in self.app_list().

        :param app_uri: App URI
        :type app_uri: :class:`str`

        :rtype: List[dict]
        """

        prepared_params = self.build_params(
            method="setActiveApp",
            params=[{"uri": app_uri}],
        )
        resp: List[dict] = self._get(params=prepared_params, service=self.service)

        return resp

    def terminate_apps(self) -> List[dict]:
        """
        Terminate all apps.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="terminateApps")
        resp: List[dict] = self._get(params=prepared_params, service=self.service)

        return resp
