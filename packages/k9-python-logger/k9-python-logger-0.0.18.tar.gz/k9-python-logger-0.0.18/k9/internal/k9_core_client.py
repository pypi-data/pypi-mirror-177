import logging
from dataclasses import dataclass
from os import environ

from requests.utils import parse_dict_header
import requests


@dataclass
class K9CoreResponse:
    id: str
    message: str
    app_name: str
    correlation_id: str
    span_id: str
    log_level: str
    
@dataclass
class K9CoreError():
    payload: dict
    status_code: int
    message: dict


class K9Core:
    host: str
    token: str

    def __init__(self):
        self.host = f"{environ.get('K9_CORE_HOST')}/api/v1"
        self.token = f"{environ.get('K9_TOKEN')}"

    def send_request(self, message):
            try:
                r = None
                r = requests.post(f"{self.host}/log", data=message, headers=parse_dict_header(f'XK9Token="{self.token}"'))
                if r.ok:
                    result = r.json()
                    return K9CoreResponse(**result)
                else:
                    raise Exception(message="Failed to integrate with k9 {}".format(r.status_code))
            except Exception as error:
                logging.error("Invalid payload: {}".format(error))
                return K9CoreError(message=message,status_code=None if r == None else r.status_code, payload=message)
