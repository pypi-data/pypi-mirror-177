from typing import List

from coiote.utils import ApiEndpoint, api_call
from coiote.v3.model.data_model import DeviceDataEntry


class DataModel(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="cachedDataModels")

    @api_call(DeviceDataEntry)
    def get_device_datamodel(self, device_id: str, parameters=[]) -> List[DeviceDataEntry]:
        return self.session.get(super()._make_url(f"/{device_id}"), params={"parameters": parameters})

    def get_device_parameter(self, device_id: str, parameter_key: str) -> List[DeviceDataEntry]:
        datamodel = self.get_device_datamodel(
            device_id=device_id, parameters=[parameter_key])
        return datamodel
