import logging
import os
from typing import Self

import mysql.connector.aio
from mysql.connector.aio.abstracts import MySQLCursorAbstract
from mysql.connector.errors import IntegrityError

from src.errors.database import (
    DatabaseConnectionError,
    DatabaseProjectAlreadyExistsError,
    DatabaseUserAlreadyExistsError,
)
from src.models.user import DBUserModel

HOST = os.getenv("DB_HOST")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_DATABASE")
PORT = os.getenv("DB_PORT")


class DatabaseInterface:
    def __init__(
        self,
        host: str = HOST,
        user: str = USER,
        password: str = PASSWORD,
        database: str = DATABASE,
        port: int | str = PORT,
    ):
        self.host: str = host
        self.user: str = user
        self.password: str = password
        self.database: str = database
        self.port: int = port if isinstance(port, int) else int(port)
        self.mysql: None | mysql.connector.aio.MySQLConnectionAbstract = None

    async def __connect(self) -> None:
        """Establish connection to database"""
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
            raise DatabaseConnectionError(
                message="Could not establish connection to database"
            )

    async def __aenter__(self) -> Self:
        """Enter context manager and establish connection to database"""
        await self.__connect()
        return self

    async def __close(self) -> None:
        """Close connection to database"""
        if self.mysql:
            await self.mysql.close()
            logging.info(f"Closed connection to database at {self.host}")

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        """Exit context manager and close connection to database"""
        await self.__close()

    async def __cursor(self) -> MySQLCursorAbstract:
        """Return cursor for database interaction"""
        return await self.mysql.cursor(dictionary=True)

    async def __get_user_by_value(
        self,
        query_value: str,
        column_name: str,
        cursor: MySQLCursorAbstract | None = None,
    ) -> DBUserModel | None:
        """Get user by value from database"""
        logging.debug("Getting user by value")
        if cursor is None:
            cursor: MySQLCursorAbstract = await self.__cursor()
        query = f"SELECT * FROM users WHERE {column_name} = %s"
        await cursor.execute(query, (query_value,))
        result = await cursor.fetchone()
        logging.debug(f"Result: {result}")
        return DBUserModel(**result) if result else None

    async def get_user_by_username(
        self, username: str, cursor: MySQLCursorAbstract | None = None
    ) -> DBUserModel | None:
        """Get user by username from database"""
        logging.debug("Getting user by username")
        return await self.__get_user_by_value(username, "username", cursor=cursor)

    async def get_user_by_email(
        self, email: str, cursor: MySQLCursorAbstract | None = None
    ) -> DBUserModel | None:
        """Get user by email from database"""
        logging.debug("Getting user by email")
        return await self.__get_user_by_value(email, "email", cursor=cursor)

    async def get_user_by_username_and_id(
        self, username: str, user_id: int, cursor: MySQLCursorAbstract | None = None
    ) -> DBUserModel | None:
        logging.debug("Getting user by username and id")
        if cursor is None:
            cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                SELECT * 
                FROM users 
                WHERE username = %s AND id = %s
                """
        await cursor.execute(query, (username, user_id))
        result = await cursor.fetchone()
        logging.debug(f"Result: {result}")
        return DBUserModel(**result) if result else None

    async def save_user(self, username: str, email: str, password: bytes) -> None:
        """Save user to database or throw an exception if user already exists"""
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                INSERT INTO users 
                (username, email, password) 
                VALUES (%s, %s, %s)
                """
        try:
            await cursor.execute(query, (username, email, password))
            await self.mysql.commit()
        except IntegrityError:
            raise DatabaseUserAlreadyExistsError()

    async def update_password(self, user_id: int, new_password: bytes) -> None:
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                UPDATE users 
                SET password = %s 
                WHERE id = %s
                """
        await cursor.execute(query, (new_password, user_id))
        await self.mysql.commit()

    async def get_projects(self, user_id: int):
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                SELECT id, name 
                FROM projects 
                WHERE owner_id = %s
                """
        await cursor.execute(query, (user_id,))
        return await cursor.fetchall()

    async def get_project(self, owner_id: int, project_id: int):
        # TODO refactor to query on project_id only
        # TODO refactor to return a model
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                SELECT stages.id, stages.name, stages.last_updated
                FROM projects
                LEFT JOIN stages on projects.id = stages.project_id 
                WHERE projects.id = %s AND projects.owner_id = %s
                """
        await cursor.execute(
            query,
            (
                project_id,
                owner_id,
            ),
        )
        return await cursor.fetchone()

    async def create_project(self, owner_id: int, project_name: str):
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                INSERT INTO projects
                (name, owner_id)
                VALUES (%s, %s)
                """
        try:
            await cursor.execute(query, (project_name, owner_id))
            await self.mysql.commit()
        except IntegrityError:
            raise DatabaseProjectAlreadyExistsError()

    async def get_project_price(self, project_id):
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                SELECT days, seconds, price 
                FROM stages WHERE project_id = %s
                """
        await cursor.execute(query, (project_id,))
        return await cursor.fetchall()

    async def get_project_price_and_paid(self, owner_id, project_id):
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                SELECT stages.days, stages.seconds, stages.price, stages.paid_eur, stages.paid_cents
                FROM projects
                LEFT JOIN stages on project.id = stages.project_id
                WHERE projects.id = %s AND projects.owner_id = %s
                """
        await cursor.execute(
            query,
            (
                project_id,
                owner_id,
            ),
        )
        return await cursor.fetchall()

    async def update_paid_amount(self, stage_id, eur, cents):
        cursor: MySQLCursorAbstract = await self.__cursor()
        query = """
                UPDATE stages 
                SET paid_cents = paid_cents + %s,
                    paid_eur = paid_eur + FLOOR(paid_cents / 100) + %s
                    paid_cents = paid_cents % 100
                WHERE id = %s
                """
        await cursor.execute(
            query,
            (
                cents,
                eur,
                stage_id,
            ),
        )
        await self.mysql.commit()
