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

    async def get_stage(self):
        async with DatabaseInterface() as db:
            await self.project_service.authorize(self.project_id, db)
            return await db.get_stage(self.stage_id)


    async def receive_payment(self, total_amount: FloatPayment | IntPayment):
        await self.project_service.authorize(self.project_id)
        eur = int(total_amount // 1)
        cents = int((total_amount % 1) * 100)
        async with DatabaseInterface() as db:
            await db.update_paid_amount(stage_id=self.stage_id, eur=eur, cents=cents)
