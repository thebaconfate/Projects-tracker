import os
import mysql.connector.aio
import logging


class DatabaseInterface:

    def __init__(
        self,
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        port=os.getenv("MYSQLPORT"),
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.mysql = None

    async def __connect(self):
        try:
            self.mysql = await mysql.connector.aio.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            logging.info(f"Connected to database at {self.host}")
        except mysql.connector.Error as e:
            logging.error(
                f"Failed to connect to database at {self.host} with error message:\n {e}"
            )
            raise Exception("Database error")

    async def __aenter__(self):
        await self.__connect()
        return self

    async def __close(self):
        if self.mysql:
            await self.mysql.close()
            logging.info(f"Closed connection to database at {self.host}")

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.__close()

    async def __cursor(self):
        return await self.mysql.cursor(dictionary=True)

    async def save_user(self, username, email, password):
        cursor = await self.__cursor()
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        await cursor.execute(query, (username, email, password))
        await self.mysql.commit()
