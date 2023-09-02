from src.classes.requestshandlers.delhandler import Delhandler
from src.classes.requestshandlers.gethandler import GetHandler
from src.classes.requestshandlers.inithandler import Inithandler
from src.classes.requestshandlers.posthandler import Posthandler
from src.classes.requestshandlers.puthandler import Puthandler

''' Factory class; might be useful in the future '''


class HandlerFactory():

    def create_del_handler(self):
        return Delhandler()

    def createPutHandler(self):
        return Puthandler()

    def createPostHandler(self):
        return Posthandler()

    def createGetHandler(self):
        return GetHandler()

    def createInitHandler(self):
        return Inithandler()
