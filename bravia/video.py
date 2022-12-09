"""
video
~~~~~

Module for the video service.
"""

from typing import List

from bravia import Bravia


class Video(Bravia):
    """
    Provides methods to interact with the Video
    service.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = "video"

    @property
    def picture_quality_settings(self, target=None) -> List[dict]:
        """
        Get picture quality settings.

        :rtype: List[dict]
        """

        target_params = [{"target": target}] if target else [{"target": ""}]

        params = {
            "method": "getPictureQualitySettings",
            "version": "1.0",
            "id": self._rand_id(),
            "params": target_params,
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def set_picture_quality_settings(self, **kwargs) -> List[dict]:
        """
        `Not implemented`

        Set picture quality settings.

        :rtype: List[dict]
        """

        params = {
            "method": "setPictureQualitySettings",
            "version": "1.0",
            "id": self._rand_id(),
            "params": [{"settings": [{"value": "2", "target": "color"}]}],
        }

        resp: List[dict] = self._set(params=params, service=self.service)

        return resp
