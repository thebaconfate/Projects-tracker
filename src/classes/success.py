
from src.classes.troubleshooter import Troubleshooter


class Success(Troubleshooter):
    
    def __init__(self, status, result):
        super().__init__(status, result)

    def get_result(self):
        return self.message