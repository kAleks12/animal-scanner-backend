import logging
import string
from datetime import timedelta, datetime
from random import choice
from typing import Literal
from uuid import UUID
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import BaseModel

from src.shared.exceptions import AuthException
from src.utils.config_parser import parser

bearer = HTTPBearer(scheme_name='Bearer')
logger = logging.getLogger("Token-Service")


class TokenPayload(BaseModel):
    sub: str
    exp: datetime

    def to_dict(self):
        return {
            'sub': self.sub,
            'exp': self.exp
        }


class ResetTokenPayload(BaseModel):
    sub: str
    code: str
    exp: datetime

    def to_dict(self):
        return {
            'sub': self.sub,
            'code': self.code,
            'exp': self.exp
        }


class RegisterTokenPayload(BaseModel):
    sub: str
    code: str

    def to_dict(self):
        return {
            'sub': self.sub,
            'code': self.code
        }


def check_access_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict[str, str]:
    return validate_token(credentials.credentials, 'access')


def check_refresh_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict[str, str]:
    return validate_token(credentials.credentials, 'refresh')


def generate_random_string() -> str:
    length = int(parser.get_attr("auth", "random_string_length"))
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(characters) for _ in range(length))


def generate_token(user_id: str, token_type: Literal['access', 'refresh']) -> str:
    exp_delta = int(parser.get_attr("auth", f'{token_type}_token_exp_min'))
    exp = datetime.utcnow() + timedelta(minutes=exp_delta)
    payload = TokenPayload(sub=user_id, exp=exp)
    token_secret = parser.get_attr("auth", f'{token_type}_token_secret')

    return jwt.encode(payload.to_dict(), token_secret, algorithm='HS512')


def generate_reset_token(user_id: str, code: str, exp_delta: int) -> str:
    exp = datetime.utcnow() + timedelta(minutes=exp_delta)
    payload = ResetTokenPayload(sub=user_id, code=code, exp=exp)
    token_secret = parser.get_attr("auth", "reset_token_secret")

    return jwt.encode(payload.to_dict(), token_secret, algorithm='HS512')


def generate_register_token(user_id: str, code: str) -> str:
    payload = RegisterTokenPayload(sub=user_id, code=code)
    token_secret = parser.get_attr("auth", "register_token_secret")

    return jwt.encode(payload.to_dict(), token_secret, algorithm='HS512')


def validate_token(token: str, token_type: Literal['access', 'refresh', 'register', 'reset']) -> dict[str, str]:
    token_secret = parser.get_attr("auth", f'{token_type}_token_secret')
    payload = jwt.decode(token, token_secret, algorithms='HS512')
    exp = datetime.utcfromtimestamp(payload["exp"])
    if exp < datetime.utcnow():
        logger.info(f"Failed to authenticate user {payload['sub']}. Token expired")
        raise AuthException("INVALID TOKEN", "Token has expired")

    return payload
