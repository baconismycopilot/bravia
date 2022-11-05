"""
av_control
==========

Module for the avControl service.
"""

from .bravia import Bravia


class AvContent(Bravia):
    r"""
    Provides methods to interact with the avControl
    service.

    :param \*\*kwargs: Arguments that Bravia takes.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = "avContent"

    def get_content_count(self):
        """
        Get the number of external inputs.

        :return:
        """

        params: dict = {
            "method": "getContentCount",
            "id": self._rand_id(),
            "params": [{"source": "extInput:hdmi"}],
            "version": "1.1"
        }

        resp = self._get(params=params, service=self.service)

        return resp

    def get_content_list(self):
        """
        Get content list.
        :return:
        """

        params = {
            "method": "getContentList",
            "id": self._rand_id(),
            "params": [{
                "stIdx": 0,
                "cnt": 50,
                "uri": "extInput:hdmi"
            }],
            "version": "1.5"
        }

        resp = self._get(params=params, service=self.service)

        return resp
