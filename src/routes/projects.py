from fastapi import APIRouter

from src.classes.services.projectservice import ProjectService


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/all")
async def get_projects():
    # TODO refactor this to use the user id of the logged in user.
    return await ProjectService().get_all_projects(1)


@router.get("/")
async def get_project(project_id: int):
    return await ProjectService().get_project(project_id)


@router.get("/total_price")
async def get_total_price(project_id):
    return await ProjectService().get_total_price(project_id)
