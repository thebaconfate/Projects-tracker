
import sys
from pytz import timezone


class Inithandler():

    def __init__(self, db):
        self.db = db

    def init_tables(self):
        print('init tables')
        cursor = self.db.connection.cursor()
        cursor.execute("CALL init")
        self.db.connection.commit()
        cursor.close()

    def drop_tables(self):
        print('drop tables')
        cursor = self.db.connection.cursor()
        cursor.execute("CALL clean")
        self.db.connection.commit()
        cursor.close()

 
