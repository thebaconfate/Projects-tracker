from .requestshandlers.delhandler import Delhandler
from .requestshandlers.gethandler import GetHandler
from .requestshandlers.inithandler import Inithandler
from .requestshandlers.posthandler import Posthandler
from .requestshandlers.puthandler import Puthandler

''' main requests handler class'''


class Requesthandler(Delhandler, Puthandler, Posthandler, GetHandler, Inithandler):
    def __init__(self, db, standard_tz):
        super().__init__(db)
        self.db = db
        self.standard_tz = standard_tz
