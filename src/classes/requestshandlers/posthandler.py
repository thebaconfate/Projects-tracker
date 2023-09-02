from datetime import datetime
from src.classes.models.user import User
from src.classes.database.databaseinterface import DatabaseInterface
from src.classes.schemas.projectschema import ProjectSchema
from src.classes.schemas.stageschema import StageSchema
from src.classes.schemas.userschema import UserSchema
from src.classes.requestshandlers.gethandler import GetHandler
from src.classes.customerrors.inputerror import InputException
from flask_login import login_user, logout_user


'''class to delegate requests that add, and update data.'''


class Posthandler(GetHandler):
    # verifies the structure of the payload

    def register(self, payload):
        schema = UserSchema()
        user = schema.load(payload, partial=('id', 'name'))
        with DatabaseInterface() as db:
            retrieved_user = db.get_user_by_mail(user.email)
            if retrieved_user is None:
                user.hash_password()
                db.insert_user(user.name, user.email, user.password)
                retrieved_user = db.get_user_by_mail(user.email)
            else:
                raise InputException('user already exists')
        user.id = retrieved_user[0]
        login_user(user)

    def login(self, payload):
        schema = UserSchema()
        user = schema.load(payload, partial=('id', 'name'))
        with DatabaseInterface() as db:
            retrieved_user = db.get_user_by_mail(user.email)
        try:
            registered_user = User(
                id=retrieved_user[0],
                name=retrieved_user[1],
                email=retrieved_user[2],
                password=retrieved_user[3])
            if registered_user.check_password(user.password):
                login_user(registered_user)
        except Exception:
            raise InputException('invalid credentials')

    def logout(self):
        logout_user()

    def create_project(self, payload, user):
        schema = ProjectSchema()
        project = schema.load(payload, partial=('id', 'owner_id'))
        with DatabaseInterface() as db:
            retrieved_project = db.get_project_by_name(project.name, user.id)
            if retrieved_project is None:
                db.insert_project(project.name, user.id)
            else:
                raise InputException('project already exists for user')

    def create_stage(self, payload, project_id, user):
        schema = StageSchema()
        stage = schema.load(payload, partial=(
            'id', 'project_id', 'last_updated', 'price', 'days', 'seconds'))
        with DatabaseInterface() as db:
            retrieved_stage = db.get_stage_by_name(
                stage.name, project_id, user.id)
            if retrieved_stage is None:
                stage.last_updated = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                db.insert_stage(stage.name, project_id, stage.days,
                                stage.seconds, stage.price, stage.last_updated)
            else:
                raise InputException('stage already exists within project')
