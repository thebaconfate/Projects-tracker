from typing import Annotated
from fastapi import Depends, APIRouter, Response, status
from src.models.stage import NewStageModel
from src.services.stageservice import StageService
from src.models.payment import FloatPayment, IntPayment
from src.services.authservice import authenticated
from src.models.user import DBUserModel

router = APIRouter(
    prefix="/projects/{project_id}/stage",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def create_stage(
    project_id: str,
    stage_name: str,
    user: Annotated[DBUserModel, Depends(authenticated)],
):
    # TODO: Refactor this, it is broken
    print("fired stage creation")
    await StageService(user.id, project_id=int(project_id)).create_stage(stage_name)
    return Response(
        status_code=status.HTTP_201_CREATED,
        content=f"Stage {stage_name} created successfully for project: {project_id}",
    )


@router.get("/{stage_id}/")
async def get_stage(
    project_id: int, stage_id: int, user: Annotated[DBUserModel, Depends(authenticated)]
):
    return await StageService(user.id, project_id, stage_id).get_stage()


@router.post("/{stages_id}/make_payment/")
async def make_payment(
    project_id: int,
    stages_id: int,
    payment: FloatPayment | IntPayment,
    user: Annotated[DBUserModel, Depends(authenticated)],
):
    await StageService(user.id, project_id, stages_id).receive_payment(payment)
    return Response(status_code=status.HTTP_200_OK, content="Payment made successfully")
