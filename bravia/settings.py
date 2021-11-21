"""
Put your settings in this file. Do not change the key
names.
"""

from pydantic import BaseSettings



settings: dict = {
    "protocol": "http",
    "base": "/sony",
    "ip": "192.168.50.220",
}


class Settings(BaseSettings):
    protocol: str
    base: str
    ip: str