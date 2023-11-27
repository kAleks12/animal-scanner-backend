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
    UNKNOWN_ERROR = ExceptionInfoValue('UNKNOWN_ERROR', status.HTTP_500_INTERNAL_SERVER_ERROR)
    ENTITY_NOT_FOUND = ExceptionInfoValue('ENTITY_NOT_FOUND', status.HTTP_404_NOT_FOUND)
    INVALID_CREDENTIALS = ExceptionInfoValue('INVALID_CREDENTIALS', status.HTTP_401_UNAUTHORIZED)
    USER_NOT_ACTIVE = ExceptionInfoValue('USER_NOT_ACTIVE', status.HTTP_401_UNAUTHORIZED)
    USER_EXISTS = ExceptionInfoValue('USER_EXISTS', status.HTTP_409_CONFLICT)
    INVALID_TOKEN = ExceptionInfoValue('INVALID_TOKEN', status.HTTP_401_UNAUTHORIZED)
    TOKEN_EXPIRED = ExceptionInfoValue('TOKEN_EXPIRED', status.HTTP_401_UNAUTHORIZED)
    ALREADY_ACTIVE = ExceptionInfoValue('ALREADY_ACTIVE', status.HTTP_409_CONFLICT)
    INVALID_DATA = ExceptionInfoValue('INVALID_DATA', status.HTTP_400_BAD_REQUEST)
    INTEGRITY_ERROR = ExceptionInfoValue('INTEGRITY_ERROR', status.HTTP_400_BAD_REQUEST)
    DOES_NOT_EXIST = ExceptionInfoValue('DOES_NOT_EXIST', status.HTTP_400_BAD_REQUEST)


