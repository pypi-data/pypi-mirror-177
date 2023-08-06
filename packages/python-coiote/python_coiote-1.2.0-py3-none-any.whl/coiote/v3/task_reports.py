from datetime import datetime
from typing import List, Optional
from urllib.parse import quote as sanitize_param

from coiote.utils import ApiEndpoint, api_call, ISO_INSTANT_FORMAT
from coiote.v3.model.task_reports import ExecutedTaskInfo, TaskReportBatch, TasksSummary, TaskReport


class TaskReports(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="taskReports")

    @api_call(ExecutedTaskInfo)
    def get_reports(self, query: str) -> List[ExecutedTaskInfo]:
        return self.session.get(super()._make_url(""), params={"searchCriteria": query})

    @api_call()
    def get_reports_cursor(self, query: str) -> int:
        return self.session.get(super()._make_url("/findReports"), params={"searchCriteria": query})

    @api_call(TaskReportBatch)
    def get_next_reports_batch(self, cursor_id: int, count: int) -> TaskReportBatch:
        return self.session.get(super()._make_url("/moreReports"), params={"cursor": cursor_id, "count": count})

    @api_call(TaskReport)
    def find_reports_since(self,
                           since: datetime,
                           taskId: Optional[str] = None,
                           deviceId: Optional[str] = None,
                           limit: int = 512,
                           polling_interval_seconds: Optional[int] = None,
                           only_direct_tasks: bool = False) -> List[TaskReport]:
        params = {
            "lastUpdateTime": since.strftime(ISO_INSTANT_FORMAT),
            "taskId": taskId,
            "deviceId": deviceId,
            "limit": limit,
            "pollingInterval": polling_interval_seconds,
            "directTasksOnly": only_direct_tasks
        }
        return self.session.get(super()._make_url("/findSince"), params=params)

    @api_call(TasksSummary)
    def get_task_summary(self, task_id: str) -> TasksSummary:
        return self.session.get(super()._make_url("/summary"), params={"taskId": task_id})

    @api_call(TaskReport)
    def get_report_for_device_task(self, task_id: str, device_id: str) -> TaskReport:
        task_id = sanitize_param(task_id)
        return self.session.get(super()._make_url(f"/{task_id}/{device_id}"))
