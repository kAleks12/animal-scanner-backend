import string
from enum import Enum

from pydantic.main import create_model
from starlette import status


class ExceptionInfoValue:
    key: str
    code: int
    response_schema: dict[int, dict[str, any]]

    def __init__(self, key: str, code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.key = key
        self.code = code
        model_name = string.capwords(key.replace('_', ''))
        self.response_schema = {code: {"model": create_model(model_name, key=(str, key), details=(str, ...))}}


class ExceptionInfo(Enum):
    VALIDATION_ERROR = ExceptionInfoValue('VALIDATION_ERROR', status.HTTP_422_UNPROCESSABLE_ENTITY)
    INTERNAL_SERVER_ERROR = ExceptionInfoValue('INTERNAL_SERVER_ERROR', status.HTTP_500_INTERNAL_SERVER_ERROR)
    UNKNOWN_ERROR = ExceptionInfoValue('UNKNOWN_ERROR', status.HTTP_500_INTERNAL_SERVER_ERROR)

