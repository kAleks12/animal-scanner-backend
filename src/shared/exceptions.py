from starlette import status


class GenericException(Exception):
    def __init__(self, key: str, message: str, code: int):
        self.message = message
        self.code = code
        self.key = key


class AuthException(GenericException):
    def __init__(self, key: str, message: str):
        super().__init__(key, message, status.HTTP_403_FORBIDDEN)


class NotFoundException(GenericException):
    def __init__(self, message: str):
        super().__init__("DOES_NOT_EXIST", message, status.HTTP_404_NOT_FOUND)


class InvalidDataException(GenericException):
    def __init__(self, message: str):
        super().__init__("INVALID_DATA", message, status.HTTP_400_BAD_REQUEST)


class BadRequestException(GenericException):
    def __init__(self, message: str, key: str = "BAD_REQUEST", code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(key, message, code)
