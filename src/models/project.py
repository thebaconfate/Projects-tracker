from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class BaseProjectModel(BaseModel):
    name: str


class NewProjectModel(BaseProjectModel):
    pass


class ProjectOwnerModel(BaseModel):
    owner_id: int


class DBProjectModel(BaseProjectModel):
    id: int
    owner_id: Optional[int] = None


class ProjectPriceModel(BaseModel):
    days: int
    seconds: int
    price: float


class ProjectPaidModel(BaseModel):
    paid_eur: int
    paid_cents: int


class SummarizedStageModel(BaseModel):
    id: int
    name: str
    last_updated: datetime


class ProjectBalanceModel(ProjectPriceModel, ProjectPaidModel):
    pass
