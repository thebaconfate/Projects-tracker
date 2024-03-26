from ast import Raise
import os
import mysql.connector.aio


class DatabaseInterface:

    async def __enter__(
        self,
        host=await os.getenv(key="DB_HOST"),
        user=await os.getenv(key="DB_USER"),
        password=await os.getenv(key="DB_PASSWORD"),
        database=await os.getenv(key="DB_DATABASE"),
        port=await os.getenv("MYSQLPORT"),
    ):
        try:
            self.mysql = await mysql.connector.aio.connect(
                host=host, user=user, password=password, database=database, port=port
            )
            return self
        except mysql.connector.Error:
            Raise(Exception("Error connecting to database"))

    async def __exit__(self, exc_type, exc_val, exc_tb):
        self.mysql.close()

    async def __cursor(self):
        return await self.mysql.cursor(dictionary=True)

    async def insert_user(self, name, email, password):
        self.__cursor().execute(
            """INSERT INTO users (name, email, password) VALUES (%s, %s, %s)""",
            (name, email, password),
        )
        self.mysql.commit()
