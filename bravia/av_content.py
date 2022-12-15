"""
av_content
~~~~~~~~~~

Module for the avControl service.
"""

from .bravia import Bravia


class AvContent(Bravia):
    r"""
    Provides methods to interact with the avControl
    service.

    :param \*\*kwargs: Arguments that :class:`Bravia` takes.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def content_count(self):
        """
        Get the number of external inputs.

        :rtype:
        """

        prepared_params = self.build_params(
            method="getContentCount",
            params=[{"source": "extInput:hdmi"}],
            version="1.1",
        )
        resp = self._get(params=prepared_params, service="avContent")

        return resp

    @property
    def content_list(self):
        """
        Get content list.

        :rtype:
        """

        prepared_params = self.build_params(
            method="getContentList",
            params=[{"stIdx": 0, "cnt": 50, "uri": "extInput:hdmi"}],
            version="1.5",
        )
        resp = self._get(params=prepared_params, service="avContent")

        return resp
