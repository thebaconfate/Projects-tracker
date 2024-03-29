from src.classes.database.interface import DatabaseInterface


class StageService:

    def __init__(self, stage_id, user_id):
        self.stage_id = stage_id
        self.user_id = user_id
        # check if the stage is owned by the user else throw an exception

    async def receive_payment(self, total_amount):
        eur = int(total_amount // 1)
        cents = int((total_amount % 1) * 100)
        async with DatabaseInterface() as db:
            await db.update_paid_amount(stage_id=self.stage_id, eur=eur, cents=cents)
