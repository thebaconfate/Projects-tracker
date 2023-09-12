from datetime import timedelta
from src.classes.models.project import Project
from src.classes.models.stage import Stage
from src.classes.schemas.projectschema import ProjectSchema
from src.classes.schemas.stageschema import StageSchema
from src.classes.database.databaseinterface import DatabaseInterface
from src.classes.schemas.userschema import UserSchema

""" class to delegate requests that fetch data to."""


class GetHandler:
    def fetch_user(self, user_id):
        with DatabaseInterface() as db:
            retrieved_user = db.get_user(user_id)
        if retrieved_user is not None:
            schema = UserSchema()
            return schema.load(
                {
                    "id": retrieved_user[0],
                    "name": retrieved_user[1],
                    "email": retrieved_user[2],
                    "password": retrieved_user[3],
                }
            )
        else:
            return None

    def get_projects(self, user):
        with DatabaseInterface() as db:
            retrieved_projects = db.get_projects(user.id)
        projects = [
            {
                "id": project[0],
                "name": project[1],
            }
            for project in retrieved_projects
        ]
        return projects

    def get_project(self, project_id, user):
        schema = ProjectSchema()
        with DatabaseInterface() as db:
            retrieved_project = db.get_project(project_id, user.id)
        project = Project(
            id=retrieved_project[0],
            name=retrieved_project[1],
            owner_id=retrieved_project[2],
        )
        return schema.dump(project)

    # * get all stages from a user
    def get_stages(self, project_id, user):
        with DatabaseInterface() as db:
            retrieved_stages = db.get_stages(project_id, user.id)
        stages = [
            {
                "id": stage[0],
                "name": stage[1],
                "project_id": stage[2],
                "last_updated": stage[3],
            }
            for stage in retrieved_stages
        ]
        return stages

    def get_stage(self, payload, user):
        schema = StageSchema()
        print(type(payload.get("id")))
        stage = schema.load(
            payload, partial=("name","last_updated", "price", "time")
        )
        with DatabaseInterface() as db:
            retrieved_stage = db.get_stage(stage.project_id, stage.id, user.id)
            return schema.dump(
                Stage(
                    id=retrieved_stage[0],
                    name=retrieved_stage[1],
                    project_id=retrieved_stage[2],
                    time=timedelta(days=retrieved_stage[3],seconds=retrieved_stage[4]),
                    price=retrieved_stage[5],
                    last_updated=retrieved_stage[6],
                )
            )

    def calc(self, project_id, user):
        with DatabaseInterface() as db:
            retrieved_stages = db.get_time_and_price(project_id, user.id)
        result = 0
        for stage in retrieved_stages:
            days = stage[0]
            seconds = stage[1]
            price = stage[2]
            total_hours = days * 24 + seconds // 3600
            print(total_hours)
            total_mins = (seconds % 3600) // 60
            print(total_mins)
            result += total_hours * price + (total_mins // 15) * (price / 4)
        return {"total value": result}
