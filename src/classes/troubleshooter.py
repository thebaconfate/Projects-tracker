
import json


class Troubleshooter:

    def __init__(self, status, message):
        self.status = status
        self.message = message

    def get_report(self):
        return { 'status': self.status, 'message': self.message }
    

