from src.database.interface import DatabaseInterface
from datetime import timedelta


class ProjectService:
    def __init__(
        self,
    ):
        pass

    async def get_all_projects(self, user_id):
        async with DatabaseInterface() as db:
            return await db.get_projects(user_id)

    async def get_project(self, project_id):
        async with DatabaseInterface() as db:
            return await db.get_project(project_id)

    async def get_total_price(self, project_id):
        async with DatabaseInterface() as db:
            list_of_stages = await db.get_price_and_paid(project_id=project_id)
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
