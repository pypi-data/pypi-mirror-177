from dataclasses import asdict

from coiote.utils import ApiEndpoint, api_call
from coiote.v3.model.task_templates import TaskTemplateInvocation
from coiote.v3.task_reports import TaskReport


class TaskTemplates(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="tasksFromTemplates")

    @api_call()
    def run_on_device(self, device_id: str, config: TaskTemplateInvocation, execute_immediately: bool) -> None:
        return self.session.post(super()._make_url(f"/device/{device_id}"),
                                 params={"executeImmediately": execute_immediately}, json=asdict(config))

    @api_call(TaskReport)
    def run_on_device_and_await(self, device_id: str, config: TaskTemplateInvocation,
                                wait_time_seconds: int) -> TaskReport:
        return self.session.post(super()._make_url(f"/device/{device_id}"),
                                 params={"waitTimeSeconds": f"{wait_time_seconds}s"}, json=asdict(config))

    @api_call()
    def run_on_group(self, group_id: str, config: TaskTemplateInvocation) -> None:
        return self.session.post(super()._make_url(f"/group/{group_id}"), data=asdict(config))
