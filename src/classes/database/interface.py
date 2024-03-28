import os
import mysql.connector.aio
import logging

from src.classes.errors.database import DatabaseConnectionError


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
            raise DatabaseConnectionError("Database error")

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

    async def get_user_by_username(self, username, cursor=None):
        if cursor is None:
            cursor = await self.__cursor()
        query = "SELECT * FROM users WHERE username = %s"
        await cursor.execute(query, (username,))
        return await cursor.fetchone()

    async def save_user(self, username, email, password):
        cursor = await self.__cursor()
        if await self.get_user_by_username(username, cursor=cursor) is not None:
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            await cursor.execute(query, (username, email, password))
            await self.mysql.commit()
        else:
            logging.error(f"User tried to register with existing username {username}")
            raise Exception("User already exists")
