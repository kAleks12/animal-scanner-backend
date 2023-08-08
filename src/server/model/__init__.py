from typing import Literal

from fastapi import Query
from pydantic import BaseModel


class BaseOrmModel(BaseModel):
    class Config:
        from_attributes = True
        population_by_name = True


class BasePaginateParams:
    page: int = None
    items_per_page: int = None

    def has_pagination(self):
        return self.page is not None and self.items_per_page is not None


class BaseSortParams:
    sort_by: str = None
    sort_order: Literal['asc', 'desc'] = Query(default='asc')

    def has_sorting(self):
        return self.sort_by is not None
