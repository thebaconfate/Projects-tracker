import json

class WorkhoursEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

