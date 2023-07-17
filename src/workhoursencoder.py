import json
from datetime import datetime, timedelta


class WorkhoursEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            dct = {}
            dct['days'] = obj.days
            dct['seconds'] = obj.seconds
            return dct
        elif isinstance(obj, datetime):
            return obj.strftime('%d-%m-%YT%H:%M:%S%z')
        else: 
            return obj.__dict__
