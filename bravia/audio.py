"""
bravia.audio
~~~~~~~~~~~~

Module for the audio service.
"""

from typing import List

from bravia.bravia import Bravia, Response


class AudioControl(Bravia):
    r"""
    Provides methods to interact with the audio
    service.

    :param \*\*kwargs: Arguments that Bravia takes.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = "audio"

    def get_sound_settings(self) -> dict:
        """
        Get the audio settings.

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "getSoundSettings",
            "id": self.rand_id(),
            "params": [{"target": "outputTerminal"}],
            "version": "1.1"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: dict = resp.json().get("result")[0]

        return data

    def get_speaker_settings(self) -> dict:
        """
        Get the speaker settings.

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "getSpeakerSettings",
            "id": self.rand_id(),
            "params": [{"target": "tvPosition"}],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: dict = resp.json().get("result")[0]

        return data

    def get_volume_info(self) -> List[dict]:
        """
        Get information about the volume
        and mute status.

        :return: :class:`List[dict]` response
        :rtype: :class:`List[dict]`
        """

        params = {
            "method": "getVolumeInformation",
            "id": self.rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, app=self.app)
        data: List[dict] = resp.json().get("result")[0]

        return data

    def mute(self, status: str) -> str:
        """
        Set mute status.

        :param str status: on or off
        :return: :class:`List[dict]` response
        :rtype: :class:`List[dict]`
        """

        status_map: dict = {
            "off": False,
            "on": True
        }

        params = {
            "method": "setAudioMute",
            "id": self.rand_id(),
            "params": [{"status": status_map.get(status)}],
            "version": "1.0"
        }

        resp: Response = self._set(params=params, app=self.app)
        data: str = resp.json().get("result")[0]
        if data == 0:
            msg: str = f"Mute {status}."
        else:
            msg: str = data

        return msg
