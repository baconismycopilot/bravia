"""
bravia.audio
~~~~~~~~~~~~

Module for the audio service.
"""

from typing import List

from .bravia import Bravia, Response


class AudioControl(Bravia):
    r"""
    Provides methods to interact with the audio
    service.

    :param \*\*kwargs: Arguments that Bravia takes.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = "audio"

    def get_sound_settings(self) -> List[dict]:
        """
        Get the audio settings.

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "getSoundSettings",
            "id": self._rand_id(),
            "params": [{"target": "outputTerminal"}],
            "version": "1.1"
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp.json()

    def get_speaker_settings(self) -> List[dict]:
        """
        Get the speaker settings.

        :return: :class:`dict` response
        :rtype: :class:`dict`
        """

        params = {
            "method": "getSpeakerSettings",
            "id": self._rand_id(),
            "params": [{"target": "tvPosition"}],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp.json

    def get_volume_info(self) -> List[dict]:
        """
        Get information about the volume
        and mute status.

        :return: :class:`List[dict]` response
        :rtype: :class:`List[dict]`
        """

        params = {
            "method": "getVolumeInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0"
        }

        resp: Response = self._get(params=params, service=self.service)

        return resp.json()

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
            "id": self._rand_id(),
            "params": [{"status": status_map.get(status)}],
            "version": "1.0"
        }

        resp: Response = self._set(params=params, service=self.service)
        data: str = resp.json().get("result")[0]
        if data == 0:
            msg: str = f"Mute {status}."
        else:
            msg: str = data

        return msg
