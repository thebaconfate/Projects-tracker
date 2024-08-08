from fastapi import HTTPException, status
from src.models.project import ProjectPriceModel, ProjectOwnerModel
from src.errors.database import DatabaseProjectAlreadyExistsError
from src.database.interface import DatabaseInterface
from src.models.project import NewProjectModel


class ProjectService:
    def __init__(self, user_id: int):
        self.__user_id: int = user_id

    @property
    def user_id(self):
        return self.__user_id

    async def authorize(self, project_id: int, db: DatabaseInterface | None = None):
        if db is None:
            async with DatabaseInterface() as db:
                project: ProjectOwnerModel | None = await db.get_project_owner(
                    project_id
                )
        else:
            project: ProjectOwnerModel = await db.get_project_owner(project_id)
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        elif project.owner_id != self.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not the owner of the project",
            )

    async def get_all_projects(self):
        async with DatabaseInterface() as db:
            return await db.get_projects(self.user_id)

    async def get_project(self, project_id: int):
        async with DatabaseInterface() as db:
            await self.authorize(project_id, db)
            return await db.get_project(project_id)

    async def create_project(self, project: NewProjectModel):
        async with DatabaseInterface() as db:
            try:
                await db.create_project(self.user_id, project.name)
            except DatabaseProjectAlreadyExistsError():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Project already exists",
                )

    async def calculate_project_price(self, project_id: int) -> float:
        async with DatabaseInterface() as db:
            await self.authorize(project_id, db)
            list_of_stages: list[ProjectPriceModel] = await db.get_project_price(
                project_id=project_id
            )
        total_price = 0
        for stage in list_of_stages:
            hours: int = stage.days * 24 + (stage.seconds // 3600)
            minutes: int = (stage.seconds // 60) % 60
            total_price += hours * stage.price + (minutes // 15) * (stage.price / 4)
        return total_price

    async def calculate_owed_amount(self, project_id: int):
        async with DatabaseInterface() as db:
            # TODO implement this method
            pass
