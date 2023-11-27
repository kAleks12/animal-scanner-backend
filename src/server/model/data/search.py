from pydantic import BaseModel


class PositionDTO(BaseModel):
    x: float
    y: float


class PlaceDTO(BaseModel):
    value: PositionDTO
    label: str

