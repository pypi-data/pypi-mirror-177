from dataclasses import asdict

from coiote.utils import ApiEndpoint, api_call
from coiote.v3.model.tasks import ConfigurationTaskDefinition


class Tasks(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="tasks")

    @api_call()
    def configure(self, device_id: str, task_definition: ConfigurationTaskDefinition) -> str:
        return self.session.post(super()._make_url(f"/configure/{device_id}"),
                                 json={'taskDefinition': asdict(task_definition)})
