
''' class to delegate requests that fetch data to.'''


from classes.models.User import User
from classes.schemas.projectschema import ProjectSchema
from classes.schemas.userschema import UserSchema


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
        project = schema.load({"id": project_id, "owner_id": user.id}, partial=('name',))
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT * from projects WHERE id = %s AND owner_id = %s''', (project.id, project.owner_id))
        rows = cursor.fetchone()
        cursor.close()
        return schema.load({"id": rows[0], "name": rows[1], "owner_id": rows[2]})

    # * get all stages from a user
    # ! this function is currently not in use
    def get_stages(self, project_id, user):
        project = self.get_project(project_id, user) 
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT id, project_id, stage_name FROM stages where project_id = %s''', (project.id,))
        rows = cursor.fetchall()
        cursor.close()
        stages = [{"id": row[0], "project_id": row[1], "stage_name": row[2]} for row in rows]  
        return stages

    def get_stage(self, project_id, stage_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT * from stages where id = %s and project_id = %s''', (stage_id, project_id))
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            result.append({
                "stage_id": row[0],
                "stage_name": row[1],
                "project_id": row[2],
                "time": {
                    "days": row[3],
                    "seconds": row[4]
                },
                "price": row[5],
                "last_updated": row[6]
            })
        return result
