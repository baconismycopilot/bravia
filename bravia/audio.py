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

        prepared_params = self.build_params(
            method="getSoundSettings",
            params=[{"target": "outputTerminal"}],
            version="1.1",
        )
        resp: List[dict] = self._get(params=prepared_params, service=self.service)

        return resp

    @property
    def speaker_settings(self) -> List[dict]:
        """
        Get the speaker settings.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(
            method="getSpeakerSettings",
            params=[{"target": "tvPosition"}],
        )
        resp: List[dict] = self._get(params=prepared_params, service=self.service)

        return resp

    @property
    def volume_info(self) -> List[dict]:
        """
        Get information about the volume and mute status.

        :rtype: List[dict]
        """

        prepared_params = self.build_params(method="getVolumeInformation")
        resp: List[dict] = self._get(params=prepared_params, service=self.service)

        return resp

    def mute(self, status: str) -> List[dict]:
        """
        Set mute status.

        :param status: On or off
        :type status: :class:`str`

        :rtype: List[dict]
        """

        status_map: dict = {"off": False, "on": True}

        prepared_params = self.build_params(
            method="setAudioMute",
            params=[{"status": status_map.get(status)}],
        )
        resp: List[dict] = self._set(params=prepared_params, service=self.service)

        return resp
