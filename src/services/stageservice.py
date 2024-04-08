from typing import Any, Coroutine
from fastapi import HTTPException, status
from src.models.stage import DBStageModel
from src.models.payment import FloatPayment, IntPayment
from src.database.interface import DatabaseInterface
from src.services.projectservice import ProjectService


class StageService:

    def __init__(self, user_id, project_id, stage_id):
        self.__project_service = ProjectService(user_id)
        self.__project_id = project_id
        self.__stage_id = stage_id

    @property
    def project_id(self):
        return self.__project_id

    @property
    def stage_id(self):
        return self.__stage_id

    @property
    def project_service(self):
        return self.__project_service
        # check if the stage is owned by the user else throw an exception

    async def get_stage(self) -> DBStageModel | None:
        async with DatabaseInterface() as db:
            await self.project_service.authorize(self.project_id, db)
            result: DBStageModel | None = await db.get_stage(self.stage_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stage not found",
            )
        else:
            return result

    async def receive_payment(self, total_amount: FloatPayment | IntPayment):
        async with DatabaseInterface() as db:
            authorized: Coroutine[Any, Any, None] = self.project_service.authorize(
                self.project_id, db
            )
            async_stage: Coroutine[Any, Any, DBStageModel | None] = db.get_stage(
                self.stage_id
            )
            eur: int = 0
            cents: int = 0
            match total_amount:
                case FloatPayment(amount=amount):
                    eur = int(amount)
                    cents = int(amount * 100 % 100)
                case IntPayment(amount=e, cents=c):
                    eur = e + c // 100
                    cents = c % 100
                case _:
                    raise ValueError("Invalid payment type")
            await authorized
            stage = await async_stage
            print(stage)
            if stage is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Stage not found",
                )
            else:
                await db.update_paid_amount(self.stage_id, eur, cents)
