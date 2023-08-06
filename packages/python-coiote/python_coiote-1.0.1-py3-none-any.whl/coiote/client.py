from typing import Any, Optional
import requests

from .auth import Authenticator
from .v3.devices import Devices
from .v3.domains import Domains
from .v3.data_model import DataModel
from .v3.device_monitoring import DeviceMonitoring
from .v3.task_templates import TaskTemplates
from .v3.tasks import Tasks
from .v3.task_reports import TaskReports
from .device_client import DeviceClient


class Coiote:
    """
    Represents a connection to Coiote server.
    """

    def __init__(
            self,
            url: str,
            auth: Optional[Any] = None,
            api_version: str = "v3",
            verify_ssl: bool = True
    ):
        self.url = url
        self.api_version = api_version
        if self.api_version not in {"v3"}:
            raise ValueError("Only v3 API is supported right now")
        self.api_url = f"{url}/api/coiotedm/{api_version}"
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.authenticator = Authenticator(
            self.url, self.session, auth=auth)

        self.data_model: DataModel = self._make_module(DataModel)
        self.device_monitoring: DeviceMonitoring = self._make_module(DeviceMonitoring)
        self.devices: Devices = self._make_module(Devices)
        self.domains: Domains = self._make_module(Domains)
        self.task_reports: TaskReports = self._make_module(TaskReports)
        self.task_templates: TaskTemplates = self._make_module(TaskTemplates)
        self.tasks: Tasks = self._make_module(Tasks)

    def _make_module(self, module_def):
        return module_def(root_url=self.api_url, authenticator=self.authenticator, session=self.session)

    def create_device_client(self, device_id: str) -> DeviceClient:
        return DeviceClient(device_id, self)
