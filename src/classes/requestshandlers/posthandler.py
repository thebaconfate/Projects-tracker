from datetime import datetime
from functools import reduce

from pytz import timezone, utc
from src.classes.customerrors.inputerror import InputException


'''class to delegate requests that add, and update data.'''


class Posthandler():

    def __init__(self, db):
        self.db = db
        self.standard_tz = timezone('Europe/Brussels')
    # verifies the structure of the payload

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
            cursor = self.db.connection.cursor()
            cursor.execute(
                "SELECT id FROM projects WHERE EXISTS (SELECT id FROM projects WHERE project_name = %s)", (project_name,))
            project_exists = cursor.fetchone()
            project_id = None
            if project_exists is None:
                cursor.execute(
                    '''INSERT INTO projects (project_name) VALUES (%s)''', (project_name,))
                self.db.connection.commit()
                cursor.execute(
                    '''SELECT id FROM projects where project_name = %s''', (project_name,))
                project_id = cursor.fetchone()[0]
            else:
                project_id = project_exists[0]
            stages_names = []
            if project_id is not None:
                cursor.execute(
                    '''SELECT stage_name FROM stages WHERE project_id = %s''', (project_id,))
                stages_names = [tp[0] for tp in cursor.fetchall()]
            for stage in stages:
                if stage['name'] in stages_names:
                    continue
                belgian_time = timezone('Europe/Brussels')
                last_updated = datetime.strptime(
                    stage['last_updated'], '%d-%m-%YT%H:%M:%S%z').replace(tzinfo=belgian_time)
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
            raise InputException('invalid payload')

    def migrate_projects(self, payload):
        valid = self._verify_projects_payload(payload)
        if valid:
            for project in payload:
                self.migrate_stages(
                    project['name'], project['stages'], verify_payload=False)
        else:
            raise InputException('invalid payload')
