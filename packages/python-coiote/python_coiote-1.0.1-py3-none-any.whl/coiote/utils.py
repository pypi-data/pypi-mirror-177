from dataclasses import dataclass
from datetime import datetime
from dateutil import parser
import functools
from typing import Any, List, Optional
from dacite import from_dict, config
from requests import Response, Session

from coiote.auth import Authenticator
from coiote.v3.model.devices import parse_psk, DtlsPreSharedKey

TYPE_HOOKS = {
    datetime: parser.isoparse,
    DtlsPreSharedKey: parse_psk
}


@dataclass
class StringResult:
    result: str


class ApiEndpoint:
    def __init__(self,
                 root_url: str,
                 api_url: str,
                 authenticator: Authenticator,
                 session: Session):
        self.root_url = root_url
        self.authenticator = authenticator
        self.session = session
        self.api_url = api_url

    def _make_url(self, endpoint: str = "") -> str:
        return f"{self.root_url}/{self.api_url}{endpoint}"


def deserialize_one(json, dataclass: Optional[Any]):
    return from_dict(data_class=dataclass, data=json, config=config.Config(type_hooks=TYPE_HOOKS))


def deserialize(json, dataclass: Optional[Any]):
    if dataclass is None:
        return json
    elif isinstance(json, list):
        return deserialize_list(json, dataclass)
    else:
        return deserialize_one(json, dataclass)


def deserialize_list(json: List[Any], dataclass):
    return [deserialize_one(element, dataclass) for element in json]


def _safe_get_json(response: Optional[Response]):
    try:
        return response.json()
    except:
        return None


def _make_error(msg: str, response: Optional[Response]):
    json = _safe_get_json(response)
    return ValueError(f"{msg}\nHeaders:{response.headers}\nBody: {json}")


def handle_response(response: Response, dataclass: Optional[Any]):
    try:
        return deserialize(json=response.json(), dataclass=dataclass)
    except:
        if response.status_code == 404:
            return None
        elif response.status_code == 403:
            raise _make_error("Lack of required permissions", response)
        elif response.status_code == 401:
            raise _make_error(
                "Unauthorized even though request was authenticated.", response)
        elif 500 > response.status_code >= 400:
            raise _make_error("Invalid request", response)
        elif response.status_code >= 500:
            raise _make_error(
                f"Internal server error - {response.status_code}", response)
        elif response.ok:
            raise _make_error("Failed to parse the server response.", None)


def api_call(response_format: Optional[Any] = None):
    def decorator_deserialize(func):
        @functools.wraps(func)
        def wrap_with_response_handle(self: ApiEndpoint, *args, **kwargs):
            self.authenticator.authenticate()
            response = func(self, *args, **kwargs)
            return handle_response(response, response_format)

        return wrap_with_response_handle

    return decorator_deserialize
