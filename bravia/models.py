"""
bravia.models
~~~~~~~~~~~~~

Models for the different REST API responses from
the device.

These models help to easily understand
the structure from the device.
"""

from typing import List, Any

from pydantic import BaseModel


class AppModel(BaseModel):
    title: str
    uri: str
    icon: str


class SystemInfo(BaseModel):
    product: str
    region: str
    language: str
    model: str
    serial: str
    macAddr: str
    name: str
    generation: str
    area: str
    cid: str


class NetworkInfo(BaseModel):
    hwAddr: str
    netmask: str
    ipAddrV4: str
    netif: str
    ipAddrV6: str
    dns: List[str]
    gateway: str


class PowerStatus(BaseModel):
    status: str


class InterfaceInfo(BaseModel):
    modelName: str
    serverName: str
    interfaceVersion: str
    productName: str
    productCategory: str


class LEDIndicator(BaseModel):
    mode: str
    status: Any


class SupportedFunc(BaseModel):
    value: str
    option: str
