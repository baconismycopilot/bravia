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


class SystemInfoModel(BaseModel):
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


class NetworkInfoModel(BaseModel):
    hwAddr: str
    netmask: str
    ipAddrV4: str
    netif: str
    ipAddrV6: str
    dns: List[str]
    gateway: str


class PowerStatusModel(BaseModel):
    status: str


class InterfaceInfoModel(BaseModel):
    modelName: str
    serverName: str
    interfaceVersion: str
    productName: str
    productCategory: str


class LEDIndicatorModel(BaseModel):
    mode: str
    status: Any


class SupportedFuncModel(BaseModel):
    value: str
    option: str
