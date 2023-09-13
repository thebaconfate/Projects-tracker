from datetime import datetime, timedelta
from src.classes.models.project import Project
from src.classes.models.stage import Stage
from src.classes.schemas.projectschema import ProjectSchema
from src.classes.schemas.stageschema import StageSchema
from src.classes.database.databaseinterface import DatabaseInterface
from src.classes.schemas.userschema import UserSchema


class GetHandler:
    """class to delegate get requests to."""

    def fetch_user(self, user_id):
        """returns dictionary with user details given a user_id. Used for post initial authentication"""
        with DatabaseInterface() as db:
            retrieved_user = db.get_user(user_id)
        if retrieved_user is not None:
            schema = UserSchema()
            return schema.load(retrieved_user)
        else:
            return None

    def get_projects(self, user):
        """Retrieves all projects in a list of dictionaries with the project id and name."""
        with DatabaseInterface() as db:
            projects = db.get_projects(user.id)
        return projects

    def get_project(self, project_id, user):
        schema = ProjectSchema()
        with DatabaseInterface() as db:
            retrieved_project = db.get_project(project_id, user.id)
        project = Project(**retrieved_project)
        return schema.dump(project)

    # * get all stages from a user
    def get_stages(self, project_id, user):
        print("getting stages")
        with DatabaseInterface() as db:
            print("retrieving")
            retrieved_stages = db.get_stages(project_id, user.id)
            for stage in retrieved_stages:
                print(stage)
                stage["last_updated"] = stage["last_updated"].strftime(
                    "%Y-%m-%dT%H:%M:%S"
                )
        return retrieved_stages

    def get_stage(self, payload, user):
        schema = StageSchema()
        stage = schema.load(payload, partial=("name", "last_updated", "price", "time"))
        with DatabaseInterface() as db:
            retrieved_stage = db.get_stage(stage.project_id, stage.id, user.id)
        retrieved_stage["time"] = timedelta(
            retrieved_stage.pop("days"), retrieved_stage.pop("seconds")
        )
        return schema.dump(Stage(**retrieved_stage))

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
