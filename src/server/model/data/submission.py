import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.server.model import BaseOrmModel
from src.server.model.data.tag import TagDTO
from src.server.model.user.user import UserDTO


class SubmissionPayload(BaseModel):
    x: float
    y: float
    relevant_date: date
    description: Optional[str]
    tags: Optional[list[str]]


class SubmissionLightDTO(BaseOrmModel):
    id: uuid.UUID
    date: date
    x: float
    y: float
    description: Optional[str] = None


class SubmissionDTO(BaseOrmModel):
    id: uuid.UUID
    x: float
    y: float
    tags: list[TagDTO]
    date: date
    description: Optional[str] = None
    author: Optional[UserDTO] = None


class SubmissionShortDTO(BaseOrmModel):
    id: uuid.UUID
    x: float
    y: float
