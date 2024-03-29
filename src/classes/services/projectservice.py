from src.classes.database.interface import DatabaseInterface


class ProjectService:
    def __init__(
        self,
    ):
        pass

    async def get_all_projects(self, user_id):
        async with DatabaseInterface() as db:
            return await db.get_projects(user_id)
