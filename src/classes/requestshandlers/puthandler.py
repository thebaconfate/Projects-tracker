from src.classes.customerrors.inputerror import InputException


''' class to handle put requests'''


class Puthandler():

    def __init__(self, db):
        self.db = db

    def switch_stage(self, key, value):
        # TODO implement switch stage
        match key:
            case 'name':
                pass
            case 'price':
                pass
            case 'time':
                pass
            case _:
                raise InputException('invalid payload to update stage')

    def update_stage(self, project_id, stage_id, payload):
        # TODO implement this
        pass
    
    def switch_project(self, key, value):
        # TODO implement switch project
        match key:
            case 'name':
                pass
            case _:
                raise InputException('invalid payload to update project')
            
    def update_project(self, project_id, payload):
        # TODO implement this
        pass