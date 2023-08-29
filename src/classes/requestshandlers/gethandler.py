from datetime import datetime

from pytz import UTC
from classes.customerrors.inputerror import InputException
from classes.models.User import User
from classes.schemas.projectschema import ProjectSchema
from classes.schemas.stageschema import StageSchema
from classes.schemas.userschema import UserSchema

''' class to delegate requests that fetch data to.'''


class GetHandler():

    def __init__(self, db):
        self.db = db

    def fetch_user(self, user_id):
        retrieved_user = self.db.get_user(user_id)
        if retrieved_user is not None:
            schema = UserSchema()
            return schema.load({
                "id": retrieved_user[0],
                "name": retrieved_user[1],
                "email": retrieved_user[2],
                "password": retrieved_user[3]
            })
        else:
            return None

    def get_projects(self, user):
        retrieved_projects = self.db.get_projects(user.id)
        projects = [{
            "id": project[0],
            "name": project[1]
        } for project in retrieved_projects]
        return projects

    def get_project(self, project_id, user):
        retrieved_project = self.db.get_project(project_id, user.id)
        project = {
            "id": retrieved_project[0],
            "name": retrieved_project[1]
        }
        return project

    # * get all stages from a user
    def get_stages(self, project_id, user):
        retrieved_stages = self.db.get_stages(project_id, user.id)
        stages = [{
            "id": retrieved_stage[0],
            "name": retrieved_stage[1],
            "project_id": retrieved_stage[2],
            "days": retrieved_stage[3],
            "seconds": retrieved_stage[4],
            "price": retrieved_stage[5],
            "last_updated": retrieved_stage[6].replace(tzinfo=UTC).strftime('%Y-%m-%d %H:%M:%S%z')
        } for retrieved_stage in retrieved_stages]
        return stages

    def get_stage(self, project_id, stage_id, user):
        retrieved_stage = self.db.get_stage(project_id, stage_id, user.id)
        stage = {
            "id": retrieved_stage[0],
            "name": retrieved_stage[1],
            "project_id": retrieved_stage[2],
            "days": retrieved_stage[3],
            "seconds": retrieved_stage[4],
            "price": retrieved_stage[5],
            "last_updated": retrieved_stage[6].replace(tzinfo=UTC).strftime('%Y-%m-%d %H:%M:%S%z')
        }
        return stage
