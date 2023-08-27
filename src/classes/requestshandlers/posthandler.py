from datetime import datetime
from functools import reduce

from pytz import timezone, utc
from classes.schemas.userschema import UserSchema
from classes.requestshandlers.gethandler import GetHandler
from classes.customerrors.inputerror import InputException
from flask_login import login_user, logout_user


'''class to delegate requests that add, and update data.'''


class Posthandler(GetHandler):

    def __init__(self, db, standard_tz):
        self.db = db
        self.timezone = standard_tz
    # verifies the structure of the payload

    def register(self, payload):
        schema = UserSchema()
        user = schema.load(payload, partial=('id',))
        user.hash_password()
        self.db.connection.cursor()
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE EXISTS (SELECT id FROM users WHERE email = %s)", (user.email,))
        if cursor.fetchone() is not None:
            cursor.close()
            raise InputException('user already exists')
        else:
            cursor.execute('''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''',
                           (user.name, user.email, user.password))
            self.db.connection.commit()
            cursor.execute(
                '''SELECT id FROM users WHERE email = %s''', (user.email,))
            user.id = cursor.fetchone()[0]
            cursor.close()
            login_user(user)
            return schema.dump(user)

    def login(self, payload):
        schema = UserSchema()
        user = schema.load(payload, partial=('id', 'name'))
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT id, name, email, password FROM users WHERE email = %s''', (user.email,))
        result = cursor.fetchone()
        cursor.close()
        print(user.password)
        print(result[3])

        try:
            registered_user = schema.load(
                {"id": result[0], "name": result[1], "email": result[2], "password": result[3]})
            print(registered_user)
            print(registered_user.check_password(user.password))
            if registered_user.check_password(user.password):
                login_user(registered_user)
                registered_user.password = None
                return schema.dump(user)
        except Exception as e:
            raise e

    def logout(self):
        logout_user()

    def __verify_stages_payload(self, payload):
        result = False
        if isinstance(payload, list):
            for stage in payload:
                if not isinstance(stage, dict) or 'name' not in stage or 'time' not in stage or 'price' not in stage or 'last_updated' not in stage or 'days' not in stage['time'] or 'seconds' not in stage['time']:
                    return False
            result = True
        return result

    def _verify_projects_payload(self, payload):
        result = False
        if isinstance(payload, list):
            for project in payload:
                if not isinstance(project, dict) or 'name' not in project or 'stages' not in project or self.__verify_stages_payload(project['stages']) is False:
                    return False
            result = True
        return result

        # * migrates stage(s) from a json file to the database if they don't already exist. Also adds the project if it doesn't exist.
    # ! The migration of stages assumes the time is set in europe/brussels. However it is saved as utc in the database.
    def migrate_stages(self, project_name, stages, verify_payload=True):
        valid = True
        if verify_payload:
            valid = self.__verify_stages_payload(stages)
        if valid:
            project_id = self.add_project(project_name)
            stages_names = []
            cursor = self.db.connection.cursor()
            if project_id is not None:
                cursor.execute(
                    '''SELECT stage_name FROM stages WHERE project_id = %s''', (project_id,))
                stages_names = [tp[0] for tp in cursor.fetchall()]
            for stage in stages:
                if stage['name'] in stages_names:
                    continue
                last_updated = datetime.strptime(
                    stage['last_updated'], '%d-%m-%YT%H:%M:%S%z').replace(tzinfo=self.standard_tz)
                print(last_updated)
                last_updated = last_updated.astimezone(utc)
                print(last_updated)
                stage_seconds = stage['time']['seconds']
                stage_days = stage['time']['days']
                cursor.execute('''INSERT INTO stages (stage_name, project_id, days, seconds, stage_price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)''', (
                    stage['name'], project_id, stage_days, stage_seconds, stage['price'], last_updated))
            self.db.connection.commit()
            cursor.close()
        else:
            raise InputException('invalid stages payload')

    def migrate_projects(self, payload):
        valid = self._verify_projects_payload(payload)
        if valid:
            for project in payload:
                self.migrate_stages(
                    project['name'], project['stages'], verify_payload=False)
        else:
            raise InputException('invalid project payload')

    def create_project(self, project):
        project_name = project['name']
        cursor = self.db.connection.cursor()
        cursor.execute(
            "SELECT id FROM projects WHERE EXISTS (SELECT id FROM projects WHERE project_name = %s)", (project_name,))
        project_id = cursor.fetchone()
        if project_id is None:
            cursor.execute(
                '''INSERT INTO projects (project_name) VALUES (%s)''', (project_name,))
            self.db.connection.commit()
            cursor.execute(
                '''SELECT id FROM projects where project_name = %s''', (project_name,))
            project_id = cursor.fetchone()[0]
        cursor.close()
        return project_id

    def create_stage(self, project_id, stage):
        exists = self.get_project(project_id)
        if exists is None:
            raise InputException('Project does not exist')
        cursor = self.db.connection.cursor()
        print(stage)
        try:
            last_updated = datetime.now(tz=self.standard_tz).astimezone(utc)
            cursor.execute('''INSERT INTO stages (stage_name, project_id, days,seconds, stage_price, last_updated) VALUES (%s, %s,%s,%s, %s,%s)''',
                           (stage['name'], project_id, stage['time']['days'], stage['time']['seconds'], stage['price'], last_updated))
            self.db.connection.commit()
            print(last_updated)
            cursor.close()
        except Exception:
            cursor.close()
            raise InputException('Invalid stage payload')
