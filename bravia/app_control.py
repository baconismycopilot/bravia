"""
bravia.app_control
~~~~~~~~~~~~~~~~~~~~~

Module for the appControl service.
"""

from typing import List

from .api import BraviaBase, Response
from .models import AppModel


class AppControl(BraviaBase):
    """
    Provides methods to interact with the appControl
    service.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def app_list(self):
        """
        Get a list of applications available on the TV.

        :return: :class:`Response <Response>` object
        :rtype: requests.Response


        :return: List[bravia.models.AppModel]
        :rtype: List[bravia.models.AppModel]
        """

        params = {
            "method": "getApplicationList",
            "version": "1.0",
            "id": self._rand_id(),
            "params": []
        }
        app = "appControl"
        resp: Response = self._get(params=params, app=app)

        apps: List[AppModel] = [
            AppModel(**x) for x in resp.json().get("result")[0]
        ]

        return apps

    def get_app_status(self, app=None) -> List[dict]:
        """
        Get the status of app(s). If app is not
        specified then all apps will be returned.

        :param app: (optional) Name of app to query.
        :return: `List[dict]`
        :rtype: `List[dict]`

        Usage::

            >>> from bravia.settings import settings
            >>> from bravia.app_control import AppControl
            >>> btv = AppControl(**settings))
            >>> app_status = btv.get_app_status()
            >>> type(app_status)
            <class `list'>
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

        app = "appControl"
        resp: Response = self._get(params=params, app=app)

        if resp.json().get("error"):
            return resp.json()

        return resp.json().get("result")[0]

    def set_active_app(self, app_uri: str) -> Response:
        """
        Start an app that is in self.app_list().

        :param str app_uri: App URI
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        params = {
            "method": "setActiveApp",
            "id": self._rand_id(),
            "params": [{
                "uri": app_uri
            }],
            "version": "1.0"
        }
        app = "appControl"
        resp: Response = self._get(params=params, app=app)

        return resp.dict()

    def terminate_apps(self) -> Response:
        """
        Terminate all terminable apps. This is terminal.

        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        params = {
            "method": "terminateApps",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        app = "appControl"
        resp: Response = self._get(params=params, app=app)

        return resp
