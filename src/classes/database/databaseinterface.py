import mysql.connector
import os


class DatabaseInterface:
    def __enter__(self):
        self.mysql = mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE"),
            port=os.getenv("MYSQLPORT"),
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.mysql.close()

    def __cursor(self):
        return self.mysql.cursor(dictionary=True)

    def __commit(self):
        self.mysql.commit()
