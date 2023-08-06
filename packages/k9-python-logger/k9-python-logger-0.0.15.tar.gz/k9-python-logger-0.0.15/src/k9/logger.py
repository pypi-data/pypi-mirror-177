import logging
from dataclasses import dataclass
import json
from enum import Enum
from typing import Generic, List, TypeVar

from k9.internal.k9_core_client import K9Core
from jsonschema import Draft7Validator
import uuid

logging.basicConfig(
    format='[K9-%(levelname)s] msg=%(message)s', level=logging.DEBUG)

T = TypeVar("T")


class Schema(Enum):
    STANDART = "standart"


@dataclass
class ErrorMessage:
    path: str
    value: str
    message: str


LogErrors = List[ErrorMessage]


@dataclass
class Teste:
    A: str
    B: int


@dataclass
class InfraProperties:
    k8s_cluster_name: str
    k8s_container_name: str
    k8s_container_id: str
    k8s_namespace: str
    k8s_deployment: str
    docker_id: str
    ip: str
    hostname: str

    # def __str__(self):
    #     return f'{self.__dict__}'


@dataclass
class LogMessage(Generic[T]):
    app_name: str
    correlation_id: str
    log_level: int
    message: str
    span_id: str
    # infrastructure: InfraProperties
    # attributes: T

    def __str__(self):
        msg = {
            "app_name": self.app_name,
            "log_level": self.log_level,
            "correlation_id": self.correlation_id,
            "message": self.message,
            "span_id": self.span_id
        }
        return f'{msg}'


class LogError:
    schema: Schema
    details = LogErrors

    def __init__(self, schema: Schema, details: LogErrors):
        self.schema = schema
        self.details = details

    def __str__(self):
        return f'[k9-log-error] schema="{self.schema}" errors={self.details}'


class K9Logger:
    schema: Draft7Validator
    app_name: str

    def __init__(self, app_name: str):
        self.app_name = app_name

    def __get_message(self, message: str, log_level: int, correlation_id: str, span_id: str):
        args = {
            "app_name": self.app_name,
            "log_level": logging.getLevelName(log_level),
            "correlation_id": correlation_id,
            "message": message,
            "span_id": span_id
        }

        return LogMessage(**args)

    def log(self, message, log_level, correlation_id=None, span_id=None):
        msg = self.__get_message(
            message=message, correlation_id=correlation_id, log_level=log_level, span_id=span_id)
        K9Core().sendRequest(message=json.dumps(msg.__dict__))
        logging.log(level=log_level, msg=msg)
        
    def info(self, message, **kwargs):
        self.log(message, logging.INFO, **kwargs)
    
    def error(self, message, **kwargs):
        self.log(message, logging.ERROR, **kwargs)
    
    def debug(self, message, **kwargs):
        self.log(message, logging.DEBUG, **kwargs)
        
    def fatal(self, message, **kwargs):
        self.log(message, logging.FATAL, **kwargs)

    def warning(self, message, **kwargs):
        self.log(message, logging.WARNING, **kwargs)
        