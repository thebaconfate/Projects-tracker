from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends
from src.services.authservice import authenticated
from models.user import DBUserModel

router = APIRouter(
    prefix="/projects/{project_id}/stage",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{stage_id}/")
async def get_stages(
    project_id: int,
    stage_id: int,
    user: Annotated[DBUserModel, Depends(authenticated)]
):
    return "get_stages"


@router.post("/{stages_id}/pay")
async def make_payment(
    project_id: int,
    stages_id: int,
    user: Annotated[DBUserModel, Depends(authenticated)]
):
    return "pay_stage"
