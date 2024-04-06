from pydantic import BaseModel


class BaseProject(BaseModel):
    name: str


class NewProject(BaseModel):
    pass


class DBProjectModel(BaseProject):
    id: int
    owner_id: int
