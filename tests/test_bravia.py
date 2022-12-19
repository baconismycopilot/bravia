"""
Basic tests.
"""

from dataclasses import dataclass
from typing import Optional

import pytest

from bravia import Bravia, AppControl, AudioControl, AvContent, Video


@dataclass
class ConfigFixture:
    ip: str
    pre_shared_key: Optional[str]


@pytest.fixture(scope="module")
def config_fixture():
    return ConfigFixture(ip="192.168.50.218", pre_shared_key="meseeks")


def test_create_bravia(config_fixture):
    b = Bravia(ip=config_fixture.ip, pre_shared_key=config_fixture.pre_shared_key)
    assert isinstance(b, Bravia)


def test_create_app_control(config_fixture):
    b = AppControl(ip=config_fixture.ip, pre_shared_key=config_fixture.pre_shared_key)
    assert isinstance(b, AppControl)


def test_create_audio_control(config_fixture):
    b = AudioControl(ip=config_fixture.ip, pre_shared_key=config_fixture.pre_shared_key)
    assert isinstance(b, AudioControl)


def test_create_av_content(config_fixture):
    b = AvContent(ip=config_fixture.ip, pre_shared_key=config_fixture.pre_shared_key)
    assert isinstance(b, AvContent)


def test_create_video(config_fixture):
    b = Video(ip=config_fixture.ip, pre_shared_key=config_fixture.pre_shared_key)
    assert isinstance(b, Video)
