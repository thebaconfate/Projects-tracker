from datetime import datetime
from flask import logging
from src.classes.customerrors.inputerror import InputException
from src.classes.schemas.stageschema import StageSchema


''' class to handle put requests'''


class Puthandler():

    def __init__(self, db):
        self.db = db

    def switch_stage(self, cursor, key, value, stage_id):
        match key:
            case 'name':
                # TODO add a check to see if the stage name already exists
                cursor.execute(
                    '''UPDATE stages SET stage_name = %s WHERE id = %s''', (value, stage_id))
            case 'price':
                cursor.execute(
                    '''UPDATE stages SET price = %s WHERE id = %s''', (value, stage_id))
            case 'time':
                for key, value in value.items():
                    self.switch_stage(cursor, key, value, stage_id)
            case 'days':
                cursor.execute(
                    '''UPDATE stages SET days = %s WHERE id = %s''', (value, stage_id))
                last_updated = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    '''UPDATE stages SET last_updated = %s WHERE id = %s''', (last_updated, stage_id))
            case 'seconds':
                cursor.execute(
                    '''UPDATE stages SET seconds = %s WHERE id = %s''', (value, stage_id))
                last_updated = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    '''UPDATE stages SET last_updated = %s WHERE id = %s''', (last_updated, stage_id))
            case _:
                logging.error('invalid payload key to update stage')
                raise InputException('invalid payload to update stage')

    def update_stage(self, project_id, stage_id, payload, current_user):
        schema = StageSchema()
        schema.load(payload, partial=('id', 'project_id',
                    'last_updated', 'price', 'days', 'seconds', 'name'))
        old_stage = self.get_stage(project_id, stage_id, current_user)
        if old_stage is not None:
            cursor = self.db.connection.cursor()
            for key, value in payload.items():
                try:
                    self.switch_stage(cursor, key, value, stage_id)
                except InputException:
                    continue
            self.db.connection.commit()
            stage = self.get_stage(project_id, stage_id, current_user)
            cursor.close()
            return stage
        else:
            raise InputException('''Couldn't find stage''')

    def switch_project(self, cursor, key, value, project_id):
        match key:
            case 'name':
                '''To rename a project'''
                # TODO add a check to see if the project name already exists
                cursor.execute(
                    '''UPDATE projects SET name = %s WHERE id = %s''', (value, project_id))
            case _:
                raise InputException('invalid payload to update project')

    def update_project(self, project_id, payload, user):
        project = self.get_project(project_id, user)
        if project is not None:
            cursor = self.db.connection.cursor()
            for key, value in payload.items():
                try:
                    self.switch_project(cursor, key, value, project_id)
                except InputException:
                    continue
            self.db.connection.commit()
            project = self.get_project(project_id, user)
            cursor.close()
            return project
