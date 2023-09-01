from src.classes.database.databaseinterface import DatabaseInterface
from src.classes.schemas.userschema import UserSchema

''' class to delegate requests that fetch data to.'''


class GetHandler():

    def fetch_user(self, user_id):
        with DatabaseInterface() as db:
            print('fetching user')
            retrieved_user = db.get_user(user_id)
        if retrieved_user is not None:
            schema = UserSchema()
            retrieved_user = {
                'id': retrieved_user[0],
                'name': retrieved_user[1],
                'email': retrieved_user[2],
                'password': retrieved_user[3]
            }
            return schema.load(retrieved_user)
        else:
            return None

    def get_projects(self, user):
        with DatabaseInterface() as db:
            retrieved_projects = db.get_projects(user.id)
        projects = [
            {
                'id': project[0],
                'name': project[1],
                'owner_id': project[2]
            } for project in retrieved_projects
        ]
        return projects

    def get_project(self, project_id, user):
        with DatabaseInterface() as db:
            retrieved_project = db.get_project(project_id, user.id)
        project = {
            'id': retrieved_project[0],
            'name': retrieved_project[1],
            'owner_id': retrieved_project[2]
        }
        return project

    # * get all stages from a user
    def get_stages(self, project_id, user):
        with DatabaseInterface() as db:
            retrieved_stages = db.get_stages(project_id, user.id)
        stages = [
            {
                'id': stage[0],
                'name': stage[1],
                'project_id': stage[2],
                'last_updated': stage[3]
            } for stage in retrieved_stages
        ]
        return stages

    def get_stage(self, project_id, stage_id, user):
        with DatabaseInterface() as db:
            retrieved_stage = db.get_stage(project_id, stage_id, user.id)
        stage = {
            'id': retrieved_stage[0],
            'name': retrieved_stage[1],
            'project_id': retrieved_stage[2],
            'price': retrieved_stage[3],
            'days': retrieved_stage[4],
            'seconds': retrieved_stage[5],
            'last_updated': retrieved_stage[6]
        }
        return stage
