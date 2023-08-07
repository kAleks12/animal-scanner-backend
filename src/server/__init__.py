from collections import ChainMap

from src.shared.enum.exception_info import ExceptionInfo


def get_error_responses(exceptions: list[ExceptionInfo]):
    exceptions = exceptions or []

    return dict(ChainMap(*[e.value.response_schema for e in exceptions]))