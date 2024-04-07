from datetime import timedelta

from fastapi import HTTPException, status
from src.errors.database import DatabaseProjectAlreadyExistsError
from src.database.interface import DatabaseInterface
from src.models.project import NewProject


class ProjectService:
    def __init__(self, user_id: int):
        self.user_id: int = user_id

    async def get_all_projects(self):
        async with DatabaseInterface() as db:
            return await db.get_projects(self.user_id)

    async def get_project(self, project_id: int):
        async with DatabaseInterface() as db:
            owner_id = await db.get_project_owner(project_id)
            if owner_id is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Project not found",
                )
            elif owner_id["owner_id"] != self.user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is not the owner of the project",
                )
            else:
                return await db.get_project(project_id)

    async def create_project(self, project: NewProject):
        async with DatabaseInterface() as db:
            try:
                await db.create_project(self.user_id, project.name)
            except DatabaseProjectAlreadyExistsError():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Project already exists",
                )

    async def calculate_project_price(self, project_id: int):
        async with DatabaseInterface() as db:
            list_of_stages = await db.get_project_price(
                self.user_id, project_id=project_id
            )
        total_price, total_paid = 0, 0
        for stage in list_of_stages:
            stage_price = float(stage["price"])
            time = timedelta(
                days=int(stage["days"]),
                seconds=int(stage["seconds"]),
            )
            minutes = time.total_seconds() // 60
            hours = minutes // 60
            minutes = minutes % 60
            total_price += stage_price * hours
            total_price += stage_price * (minutes // 15) * (stage_price / 4)
            total_paid += float(stage["paid_eur"]) + float(stage["paid_cents"]) / 100
        total_price = round(total_price - total_paid, 2)
        return total_price

    async def calculate_owed_amount(self, project_id: int):
        async with DatabaseInterface() as db:
            pass
