
from src.classes.troubleshooter import Troubleshooter


class Errors(Troubleshooter):

    def __init__(self, status, error_code, message):
        super().__init__(status, message)
        self.location = error_code

    def get_report(self):
        report = super().get_report()
        report['location'] = self.location
        return report
