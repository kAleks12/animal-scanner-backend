import uuid
from typing import Optional

from pydantic import BaseModel

from src.server.model import BaseOrmModel
from src.server.model.user.user import UserDTO


class SubmissionPayload(BaseModel):
    x: float
    y: float
    description: str


class SubmissionLightDTO(BaseOrmModel):
    id: uuid.UUID
    x: float
    y: float
    description: Optional[str] = None


class SubmissionDTO(BaseOrmModel):
    id: uuid.UUID
    x: float
    y: float
    description: Optional[str] = None
    user: Optional[UserDTO] = None


class SubmissionShortDTO(BaseOrmModel):
    id: uuid.UUID
    x: float
    y: float
