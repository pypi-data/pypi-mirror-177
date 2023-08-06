from dataclasses import asdict, replace

from coiote.utils import ApiEndpoint, api_call
from coiote.v3.model.devices import *


class Devices(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="devices")

    @api_call()
    def get_all(self, search_criteria: Optional[str]) -> List[str]:
        return self.session.get(super()._make_url(), params={"searchCriteria": search_criteria})

    @api_call(DevicesBatchAddResponse)
    def create_batch(self, devices: List[Device]) -> DevicesBatchAddResponse:
        updated_devices = self._update_endpoint_names(devices)
        return self.session.post(super()._make_url("/batch"), json=[asdict(device) for device in updated_devices])

    @staticmethod
    def _update_properties(device_id: Optional[str], properties: Dict[str, str]) -> Dict[str, str]:
        if device_id is None:
            return properties
        else:
            return dict(properties, endpointName=device_id)

    def _update_device(self, device: Device) -> Device:
        return replace(device, id=None, properties=self._update_properties(device.id, device.properties))

    def _update_endpoint_names(self, devices: List[Device]) -> List[Device]:
        return [self._update_device(device) for device in devices]

    @api_call(DevicesFindResponse)
    def get_device_details(self, search_criteria: Optional[str] = None, fields: List[str] = [], limit: int = 100,
                           pageBookmark: Optional[str] = None) -> DevicesFindResponse:
        return self.session.get(super()._make_url("/find/details"), params={
            "searchCriteria": search_criteria,
            "fieldSelection": ",".join(fields),
            "limit": limit,
            "pageBookmark": pageBookmark
        })

    @api_call(SingleDeviceAddResponse)
    def create_one(self, device: Device) -> SingleDeviceAddResponse:
        updated = self._update_device(device)
        return self.session.post(super()._make_url(), json=asdict(updated))

    @api_call(Device)
    def get_one(self, device_id: str) -> Device:
        return self.session.get(super()._make_url(f"/{device_id}"))

    @api_call()
    def update_one(self, device_id, request: DeviceUpdateRequest) -> None:
        return self.session.put(super()._make_url(f"/{device_id}"), json=asdict(request))

    @api_call()
    def delete_one(self, device_id) -> None:
        return self.session.delete(super()._make_url(f"/{device_id}"))
