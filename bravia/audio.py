"""
bravia.audio
~~~~~~~~~~~~

Module for the audio service.
"""

from typing import List

from .bravia import Bravia


class AudioControl(Bravia):
    r"""
    Provides methods to interact with the audio
    service.

    :param \*\*kwargs: Arguments that :class:`Bravia` takes.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = "audio"

    @property
    def sound_settings(self) -> List[dict]:
        """
        Get the audio settings.

        :rtype: List[dict]
        """

        params = {
            "method": "getSoundSettings",
            "id": self._rand_id(),
            "params": [{"target": "outputTerminal"}],
            "version": "1.1",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    @property
    def speaker_settings(self) -> List[dict]:
        """
        Get the speaker settings.

        :rtype: List[dict]
        """

        params = {
            "method": "getSpeakerSettings",
            "id": self._rand_id(),
            "params": [{"target": "tvPosition"}],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    @property
    def volume_info(self) -> List[dict]:
        """
        Get information about the volume and mute status.

        :rtype: List[dict]
        """

        params = {
            "method": "getVolumeInformation",
            "id": self._rand_id(),
            "params": [],
            "version": "1.0",
        }

        resp: List[dict] = self._get(params=params, service=self.service)

        return resp

    def mute(self, status: str) -> List[dict]:
        """
        Set mute status.

        :param status: On or off
        :type status: :class:`str`

        :rtype: List[dict]
        """

        status_map: dict = {"off": False, "on": True}

        params = {
            "method": "setAudioMute",
            "id": self._rand_id(),
            "params": [{"status": status_map.get(status)}],
            "version": "1.0",
        }

        resp: List[dict] = self._set(params=params, service=self.service)

        return resp
