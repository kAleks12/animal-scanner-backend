from pydantic import BaseModel


class PlaceDTO(BaseModel):
    x: float
    y: float
    name: str
