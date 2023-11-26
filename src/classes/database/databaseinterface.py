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

    def insert_user(self, name, email, password):
        self.__cursor().execute(
            """INSERT INTO users (name, email, password) VALUES (%s, %s, %s)""",
            (name, email, password),
        )
        self.__commit()

    def get_user_by_mail(self, email):
        cursor = self.__cursor()
        cursor.execute(
            """SELECT id, name, email, password FROM users WHERE email = %s""", (email,)
        )
        user = cursor.fetchone()
        return user
