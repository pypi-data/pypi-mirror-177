from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum


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


class TransferMethod(str, Enum):
    Pull = 'Pull'
    Push = 'Push'


class TransferProtocol(str, Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    COAP = "COAP"
    COAPS = "COAPS"
    COAP_TCP = "COAP_TCP"
    COAP_TLS = "COAP_TLS"


class UpgradeStrategy(str, Enum):
    ObservationTrigger = "ObservationTrigger"
    WithoutObservations = "WithoutObservations"
    ObservationBased = "ObservationBased"
    SendBased = "SendBased"


@dataclass
class TaskParameter:
    name: str
    value: str


@dataclass
class TaskConfig:
    taskName: str
    parameters: List[TaskParameter]
    properties: Dict[str, str]
    isActive: Optional[bool] = False


@dataclass
class Task:
    id: str
    config: TaskConfig
