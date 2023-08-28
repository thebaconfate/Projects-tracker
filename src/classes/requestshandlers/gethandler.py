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
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT id, name, email, password FROM users WHERE id = %s''', (user_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            schema = UserSchema()
            return schema.load({"id": result[0], "name": result[1], "email": result[2], "password": result[3]})
        else:
            return None

    def get_projects(self, user):
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT id, name FROM projects where owner_id = %s", (user.id,))
        projects = cursor.fetchall()
        cursor.close()
        parsed_projects = [{"id": project[0], "name":project[1],
                            "owner_id": user.id} for project in projects]
        schema = ProjectSchema(many=True)
        results = schema.load(parsed_projects)
        return schema.dump(results)

    def get_project(self, project_id, user):
        schema = ProjectSchema()
        project = schema.load(
            {"id": project_id, "owner_id": user.id}, partial=('name',))
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT * from projects WHERE id = %s AND owner_id = %s''', (project.id, project.owner_id))
        rows = cursor.fetchone()
        cursor.close()
        return schema.load({"id": rows[0], "name": rows[1], "owner_id": rows[2]})

    # * get all stages from a user
    def get_stages(self, project_id, user):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT stages.id, project_id, stage_name, last_updated FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE projects.id = %s AND users.id = %s ORDER BY stages.id ASC;''', (project_id, user.id))
        rows = cursor.fetchall()
        cursor.close()
        if rows is not None:
            stages = [{"id": row[0], "project_id": row[1],
                       "stage_name": row[2], "last_updated": row[3]} for row in rows]
            return stages
        else:
            raise InputException('no stages found')

    def get_stage(self, project_id, stage_id, user):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT stages.id, stage_name, project_id, days, seconds, price, last_updated  FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE stages.id = %s AND projects.id = %s and users.id = %s ;''', (stage_id, project_id, user.id))
        row = cursor.fetchone()
        cursor.close()
        if row is not None:
            stagedct = {"id": row[0], "name": row[1], "project_id": row[2], "days": row[3],
                     "seconds": row[4], "price": row[5], "last_updated": row[6].replace(tzinfo=UTC).strftime('%Y-%m-%d %H:%M:%S%z')}
            print(stagedct)
            schema = StageSchema()
            stage = schema.load(stagedct)
            return schema.dump(stage)
