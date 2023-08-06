from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class DeviceOperation:
    pass


@dataclass
class ReadDefinition:
    key: str


@dataclass
class ReadOperation(DeviceOperation):
    read: ReadDefinition


@dataclass
class WriteDefinition:
    key: str
    value: str


@dataclass
class WriteOperation(DeviceOperation):
    write: WriteDefinition


@dataclass
class ExecuteArg:
    digit: int
    argument: Optional[str] = None


@dataclass
class ExecuteDefinition:
    key: str
    argumentList: List[ExecuteArg] = field(default_factory=list)


@dataclass
class ExecuteOperation(DeviceOperation):
    execute: ExecuteDefinition


@dataclass
class ConfigurationTaskDefinition:
    name: str
    batchRequests: bool = True
    executeImmediately: bool = True
    operations: List[DeviceOperation] = field(default_factory=list)
