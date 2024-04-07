from typing import Annotated
from fastapi import APIRouter, Depends

from src.models.project import NewProject
from src.models.user import DBUserModel
from src.services.authservice import authenticated
from src.services.stageservice import StageService
from src.services.projectservice import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_projects(user: Annotated[DBUserModel, Depends(authenticated)]):
    return await ProjectService(user.id).get_all_projects()


@router.post("/")
async def create_project(
    project: NewProject, user: Annotated[DBUserModel, Depends(authenticated)]
):
    return await ProjectService(user.id).create_project(project)


@router.get("/{project_id}")
async def get_project(
    project_id: int,
    user: Annotated[DBUserModel, Depends(authenticated)],
):
    return await ProjectService(user.id).get_project(project_id)


@router.get("/{project_id}/project_price/")
async def get_total_price(
    project_id: int, user: Annotated[DBUserModel, Depends(authenticated)]
):
    return await ProjectService(user.id).calculate_project_price(project_id)


@router.get("/{project_id}/owed_amount/")
async def get_owed_amount(
    project_id: int, user: Annotated[DBUserModel, Depends(authenticated)]
):
    return await ProjectService(user.id).calculate_owed_amount(project_id)
