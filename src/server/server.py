import logging
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.background import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.shared.enum.exception_info import ExceptionInfoValue, ExceptionInfo
from src.shared.exceptions import GenericException, AuthException
from src.utils.config_parser import parser

from src.server.router.user.auth_router import router as auth_router


class ErrorResponseContent:
    def __init__(self, key: str = None, message: str = None):
        self.key = key
        self.message = message


class ErrorResponse(JSONResponse):
    def __init__(self, content: ErrorResponseContent, code: int = 500,
                 background: Optional[BackgroundTasks] = None):
        super().__init__(content, code, background=background)

    def render(self, content: any) -> bytes:
        return super().render(vars(content))


def _get_error_response(key: str, code: int, msg: str) -> ErrorResponse:
    return ErrorResponse(
        ErrorResponseContent(key, msg),
        code,
    )


async def _exception_handler_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except GenericException as e:
        return _get_error_response(e.key, e.code, e.message)
    except ValidationError as e:
        exception = ExceptionInfo.VALIDATION_ERROR.value
        return _get_error_response(exception.key, exception.code, str(e))
    except Exception as e:
        exception = ExceptionInfo.UNKNOWN_ERROR.value
        return _get_error_response(exception.key, exception.code, str(e))


class Server:
    def __init__(self):
        self.logger = logging.getLogger('Server')
        docs = "/docs" if int(parser.get_attr('server', 'docs')) else None
        redoc = "/redoc" if int(parser.get_attr('server', 'redoc')) else None
        self.prefix = parser.get_attr('server', 'prefix')
        self.app = FastAPI(docs_url=docs, redoc_url=redoc)
        self.app.middleware("http")(_exception_handler_middleware)
        self.app.add_exception_handler(RequestValidationError, self.validation_exception_handler)
        self.routers = [auth_router]

    def wrap_cors(self):
        allowed_origins = parser.get_attr('server', 'allow_origins').split(',')
        allowed_methods = parser.get_attr('server', 'allow_methods').split(',')
        allowed_headers = parser.get_attr('server', 'allow_headers').split(',')
        self.app = CORSMiddleware(app=self.app, allow_headers=allowed_headers, allow_origins=allowed_origins,
                                  allow_methods=allowed_methods, allow_credentials=True)

    def prepare(self):
        prefix = self.prefix if self.prefix else '/api/v1'
        for router in self.routers:
            self.app.include_router(router, prefix=prefix)

    async def validation_exception_handler(self, _: Request, e: RequestValidationError):
        self.logger.error(str(e.errors()))
        return _get_error_response(ExceptionInfo.VALIDATION_ERROR.value.key, ExceptionInfo.VALIDATION_ERROR.value.code,  str(e).replace('\n', ''))
