from datetime import datetime
from flask import logging
from src.classes.customerrors.inputerror import InputException
from src.classes.schemas.stageschema import StageSchema


''' class to handle put requests'''


class Puthandler():

    def __init__(self, db):
        self.db = db

    def switch_stage(self, key, value, stage_id):
        match key:
            case 'name':
                # TODO add a check to see if the stage name already exists
                self.db.update_stage_name(stage_id, value)
            case 'price':
                self.db.update_stage_price(stage_id, value)
            case 'time':
                for key, value in value.items():
                    self.switch_stage(key, value, stage_id)
            case 'days':
                self.db.update_stage_days(stage_id, value)
                last_updated = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                self.db.update_stage_last_updated(stage_id, last_updated)
            case 'seconds':
                self.db.update_stage_seconds(stage_id, value)
                last_updated = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                self.db.update_stage_last_updated(stage_id, last_updated)
            case _:
                logging.error('invalid payload key to update stage')
                raise InputException('invalid payload to update stage')

    def update_stage(self, project_id, stage_id, payload, current_user):
        schema = StageSchema()
        schema.load(payload, partial=('id', 'project_id',
                    'last_updated', 'price', 'days', 'seconds', 'name'))
        old_stage = self.get_stage(project_id, stage_id, current_user)
        if old_stage is not None:
            for key, value in payload.items():
                try:
                    self.switch_stage(key, value, stage_id)
                except InputException:
                    continue
            stage = self.get_stage(project_id, stage_id, current_user)
            return stage
        else:
            raise InputException('''Couldn't find stage''')

    def switch_project(self, key, value, project_id):
        match key:
            case 'name':
                '''To rename a project'''
                # TODO add a check to see if the project name already exists
                self.db.update_project_name(project_id, value)
            case _:
                raise InputException('invalid payload to update project')

    def update_project(self, project_id, payload, user):
        project = self.get_project(project_id, user)
        if project is not None:
            for key, value in payload.items():
                try:
                    self.switch_project(key, value, project_id)
                except InputException:
                    continue
            project = self.get_project(project_id, user)
            return project
