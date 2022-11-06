"""
video
~~~~~

Module for the video service.
"""

from typing import List

from bravia import Bravia


class Video(Bravia):
    """
    Provides methods to interact with the appControl
    service.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = "video"

    def get_picture_quality_settings(self) -> List[dict]:
        """
        Get picture quality settings.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "getPictureQualitySettings",
            "version": "1.0",
            "id": self._rand_id(),
            "params": []
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def set_picture_quality_settings(self, **kwargs) -> List[dict]:
        """
        `Not implemented`

        Set picture quality settings.

        :return: :class:`List[dict]`
        """

        params = {
            "method": "setPictureQualitySettings",
            "version": "1.0",
            "id": self._rand_id(),
            "params": [{"settings": [{
                "value": "2",
                "target": "color"
            }]}],
        }

        resp: List[dict] = self._set(params=params, service=self.service)

        return resp
