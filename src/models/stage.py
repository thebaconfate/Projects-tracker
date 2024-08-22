from datetime import datetime
from pydantic import BaseModel


class DBStageModel(BaseModel):
    id: int
    name: str
    project_id: int
    days: int
    seconds: int
    price: float
    paid_eur: int
    paid_cents: int
    last_updated: datetime

class NewStageModel(BaseModel):
    project_id: int
    stage_name: str