from pytz import timezone
from src.classes.requestshandlers.delhandler import Delhandler
from src.classes.requestshandlers.gethandler import GetHandler
from src.classes.requestshandlers.inithandler import Inithandler
from src.classes.requestshandlers.posthandler import Posthandler
from src.classes.requestshandlers.puthandler import Puthandler

''' main requests handler class'''


class Requesthandler(Delhandler, Puthandler, Posthandler, GetHandler, Inithandler):
    def __init__(self, db, standard_tz):
        super().__init__(db)
        self.db = db
        self.standard_tz = standard_tz
