from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List

from dacite import from_dict


@dataclass
class DtlsPreSharedKey:
    pass


def parse_psk(psk_data: Dict[str, str]) -> Optional[DtlsPreSharedKey]:
    if "PlainTextPsk" in psk_data:
        return from_dict(data_class=PlaintextPsk, data=psk_data)
    elif "BinaryPsk" in psk_data:
        return from_dict(data_class=BinaryPsk, data=psk_data)
    elif "HexadecimalPsk" in psk_data:
        return from_dict(data_class=HexStringPsk, data=psk_data)
    else:
        return None


@dataclass
class PlaintextPsk(DtlsPreSharedKey):
    PlainTextPsk: str


@dataclass
class BinaryPsk(DtlsPreSharedKey):
    BinaryPsk: List[int]


@dataclass
class HexStringPsk(DtlsPreSharedKey):
    HexadecimalPsk: str


@dataclass
class Device:
    domain: Optional[str] = None
    id: Optional[str] = None
    lastSessionTime: Optional[datetime] = None
    lastContactTime: Optional[datetime] = None
    lastRegisterTime: Optional[datetime] = None
    firstRegisterTime: Optional[datetime] = None
    creationTime: Optional[datetime] = None
    ipAddress: Optional[str] = None
    serialNumber: Optional[str] = None
    oui: Optional[str] = None
    modelName: Optional[str] = None
    hardwareVersion: Optional[str] = None
    softwareVersion: Optional[str] = None
    productClass: Optional[str] = None
    manufacturer: Optional[str] = None
    description: Optional[str] = None
    friendlyName: Optional[str] = None
    securityMode: Optional[str] = None
    dtlsIdentity: Optional[str] = None
    dtlsPsk: Optional[DtlsPreSharedKey] = None
    connectorType: str = "management"
    bootstrap: bool = False
    directGroups: List[str] = field(default_factory=list)
    properties: Dict[str, str] = field(default_factory=dict)
    blacklisted: bool = False
    managementEnabled: bool = False


@dataclass
class DevicesFindResponse:
    devices: List[Device] = field(default_factory=list)
    nextPageBookmark: Optional[str] = None


@dataclass
class DeviceUpdateRequest:
    addProperties: Dict[str, str] = field(default_factory=dict)
    removeProperties: List[str] = field(default_factory=list)
    addGroups: List[str] = field(default_factory=list)
    removeGroups: List[str] = field(default_factory=list)
    blacklisted: bool = False
    managementEnabled: bool = True
    description: Optional[str] = None
    friendlyName: Optional[str] = None
    securityMode: Optional[str] = None
    dtlsIdentity: Optional[str] = None
    dtlsPsk: Optional[DtlsPreSharedKey] = None


@dataclass
class SingleDeviceAddResponse:
    id: str
    result: str


@dataclass
class DevicesAddResponse:
    id: str
    success: bool
    reason: Optional[str] = None


@dataclass
class DevicesBatchAddResponse:
    total: int
    succeeded: int
    failed: int
    results: List[DevicesAddResponse]
