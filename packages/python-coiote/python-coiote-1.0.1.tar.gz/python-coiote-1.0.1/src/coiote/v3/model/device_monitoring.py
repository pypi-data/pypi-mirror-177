from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List

ISO_INSTANT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class MonitoringStatus:
    enabled: bool


@dataclass
class Datapoint:
    date: datetime
    value: str


@dataclass
class MonitoringDataResponse:
    hasNext: bool
    lastPointTimestamp: Optional[datetime] = field(default=None)
    metadata: Dict[str, str] = field(default_factory=dict)
    data: List[Datapoint] = field(default_factory=list)
