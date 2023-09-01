from datetime import datetime
from functools import reduce

from pytz import timezone, utc
from src.classes.schemas.projectschema import ProjectSchema
from src.classes.schemas.stageschema import StageSchema
from src.classes.schemas.userschema import UserSchema
from src.classes.requestshandlers.gethandler import GetHandler
from src.classes.customerrors.inputerror import InputException
from flask_login import login_user, logout_user


'''class to delegate requests that add, and update data.'''


class Posthandler(GetHandler):

    def __init__(self, db):
        self.db = db
    # verifies the structure of the payload

    def register(self, payload):
        schema = UserSchema()
        user = schema.load(payload, partial=('id', 'name'))
        print(user)
        retrieved_user = self.db.get_user_by_mail(user.email)
        print(retrieved_user)
        if retrieved_user is None:
            user.hash_password()
            self.db.insert_user(user.name, user.email, user.password)
            retrieved_user = self.db.get_user_by_mail(user.email)
            user.id = retrieved_user[0]
            print(user)
            login_user(user)
        else:
            raise InputException('user already exists')

    def login(self, payload):
        schema = UserSchema()
        user = schema.load(payload, partial=('id', 'name'))
        retrieved_user = self.db.get_user_by_mail(user.email)
        try:
            registered_user = schema.load(
                {"id": retrieved_user[0],
                 "name": retrieved_user[1],
                 "email": retrieved_user[2],
                 "password": retrieved_user[3]})
            if registered_user.check_password(user.password):
                login_user(registered_user)
        except Exception:
            raise InputException('invalid credentials')

    def logout(self):
        logout_user()

    def create_project(self, payload, user):
        schema = ProjectSchema()
        project = schema.load(payload, partial=('id', 'owner_id'))
        retrieved_project = self.db.get_project_by_name(project.name, user.id)
        if retrieved_project is None:
            self.db.insert_project(project.name, user.id)
        else:
            raise InputException('project already exists for user')

    def create_stage(self, payload, project_id, user):
        schema = StageSchema()
        stage = schema.load(payload, partial=(
            'id', 'project_id', 'last_updated', 'price', 'days', 'seconds'))
        retrieved_stage = self.db.get_stage_by_name(
            stage.name, project_id, user.id)
        if retrieved_stage is None:
            stage.last_updated = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            self.db.insert_stage(stage.name, project_id, stage.days,
                                 stage.seconds, stage.price, stage.last_updated)
        else:
            raise InputException('stage already exists within project')
