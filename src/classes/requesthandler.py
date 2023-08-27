from pytz import timezone
from classes.requestshandlers.delhandler import Delhandler
from classes.requestshandlers.gethandler import GetHandler
from classes.requestshandlers.inithandler import Inithandler
from classes.requestshandlers.posthandler import Posthandler
from classes.requestshandlers.puthandler import Puthandler

''' main requests handler class'''


class Requesthandler(Delhandler, Puthandler, Posthandler, GetHandler, Inithandler):
    def __init__(self, db, standard_tz):
        super().__init__(db)
        self.db = db
        self.standard_tz = standard_tz
