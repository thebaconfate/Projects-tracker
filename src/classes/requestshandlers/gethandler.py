from datetime import datetime

from pytz import UTC
from ..customerrors.inputerror import InputException
from ..models.user import User
from ..schemas.projectschema import ProjectSchema
from ..schemas.stageschema import StageSchema
from ..schemas.userschema import UserSchema

''' class to delegate requests that fetch data to.'''


class GetHandler():

    def __init__(self, db):
        self.db = db

    def fetch_user(self, user_id):
        retrieved_user = self.db.get_user(user_id)
        if retrieved_user is not None:
            schema = UserSchema()
            return schema.load(retrieved_user)
        else:
            return None

    def get_projects(self, user):
        projects = self.db.get_projects(user.id)
        return projects

    def get_project(self, project_id, user):
        project = self.db.get_project(project_id, user.id)
        return project

    # * get all stages from a user
    def get_stages(self, project_id, user):
        stages = self.db.get_stages(project_id, user.id)
        return stages

    def get_stage(self, project_id, stage_id, user):
        stage = self.db.get_stage(project_id, stage_id, user.id)
        return stage
