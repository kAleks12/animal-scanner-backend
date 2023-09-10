from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from src.server.model import BaseOrmModel


class UserLoginPayload(BaseModel):
    user: str
    password: str


class UserRegisterPayload(BaseModel):
    username: Optional[str] = None
    password: str
    email: EmailStr


class ChangePasswordPayload(BaseModel):
    current_password: Optional[str] = None
    new_password: str


class UserDTO(BaseOrmModel):
    id: UUID
    username: str
    email: str
    activated: bool


class AuthSession(BaseModel):
    access_token: str

    def to_dict(self):
        return {
            "access_token": self.access_token
        }
