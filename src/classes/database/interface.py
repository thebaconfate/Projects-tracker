import os
import mysql.connector.aio
import logging
from mysql.connector.aio.abstracts import MySQLCursorAbstract
from src.classes.models.user import UserDBModel
from src.classes.errors.database import DatabaseConnectionError


class DatabaseInterface:
    def __init__(
        self,
        host: str = os.getenv("DB_HOST"),
        user: str = os.getenv("DB_USER"),
        password: str = os.getenv("DB_PASSWORD"),
        database: str = os.getenv("DB_DATABASE"),
        port: int = int(os.getenv("DB_PORT")),
    ):
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.database: str = database
        self.port: int = port
        self.mysql: None | mysql.connector.aio.MySQLConnectionAbstract = None

    async def __connect(self) -> None:
        try:
            self.mysql: mysql.connector.aio.MySQLConnectionAbstract = (
                await mysql.connector.aio.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                )
            )
            logging.info(msg=f"Connected to database at {self.host}")
        except mysql.connector.Error as e:
            logging.error(
                msg=f"Failed to connect to database at {self.host} with error message:\n {e}"
            )
            raise DatabaseConnectionError(message="Database error")

    async def __aenter__(self):
        await self.__connect()
        return self

    async def __close(self) -> None:
        if self.mysql:
            await self.mysql.close()
            logging.info(f"Closed connection to database at {self.host}")

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.__close()

    async def __cursor(self) -> MySQLCursorAbstract:
        return await self.mysql.cursor(dictionary=True)

    async def get_user_by_username(self, username, cursor=None):
        if cursor is None:
            cursor: MySQLCursorAbstract = await self.__cursor()
        query = "SELECT * FROM users WHERE username = %s"
        await cursor.execute(query, (username,))
        return UserDBModel(**await cursor.fetchone())

    async def get_user_by_email(self, email, cursor=None):
        if cursor is None:
            cursor: MySQLCursorAbstract = await self.__cursor()
        query = "SELECT * FROM users WHERE email = %s"
        await cursor.execute(query, (email,))
        return UserDBModel(**await cursor.fetchone())

    async def save_user(self, username, email, password):
        cursor: MySQLCursorAbstract = await self.__cursor()
        if (
            await self.get_user_by_username(username=username, cursor=cursor)
            is not None
        ):
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            await cursor.execute(operation=query, params=(username, email, password))
            await self.mysql.commit()
        else:
            logging.error(f"User tried to register with existing username {username}")
            raise Exception("User already exists")

    async def update_password(self, user_id, new_password):
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = "UPDATE users SET password = %s WHERE id = %s"
        await cursor.execute(query, (new_password, user_id))
        await self.mysql.commit()

    async def get_projects(self, user_id):
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = "SELECT id, name FROM projects WHERE owner_id = %s"
        await cursor.execute(query, (user_id,))
        return await cursor.fetchall()
