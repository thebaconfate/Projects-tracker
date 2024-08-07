import logging
import mysql.connector
from mysql.connector.cursor import MySQLCursor
from src.database import HOST, USER, PASSWORD, DATABASE, PORT
from src.errors.database import DatabaseConnectionError


class DatabaseInitiator:
    def __init__(
        self,
        host: str = HOST,
        user: str = USER,
        password: str = PASSWORD,
        database: str = DATABASE,
        port: int | str = PORT,
    ):
        if HOST and USER and PASSWORD and PORT:
            self.host: str = host
            self.user: str = user
            self.password: str = password
            self.database: str = database
            self.port: int = port if isinstance(port, int) else int(port)
            self.mysql: None | mysql.connector.MySQLConnection = None

    def __init_possible(self):
        return HOST and USER and PASSWORD and DATABASE

    def __enter__(self):
        if self.__init_possible():
            try:
                self.mysql = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                )
            except mysql.connector.Error as e:
                logging.error(
                    msg=f"Failed to connect to database at {self.host} with error message:\n {e}"
                )
                raise DatabaseConnectionError(
                    message="Could not establish connection to database"
                )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.mysql:
            self.mysql.close()

    def init_db(self) -> None:
        if self.__init_possible():
            cursor: MySQLCursor = self.mysql.cursor()
            create_users_table = """CREATE TABLE IF NOT EXISTS users (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VARBINARY(255) NOT NULL)
                    """
            create_projects_table = """CREATE TABLE IF NOT EXISTS projects (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    owner_id BIGINT,
                    FOREIGN KEY (owner_id) REFERENCES users(id))"""
            create_stages_table = """CREATE TABLE IF NOT EXISTS stages (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    project_id BIGINT,
                    days BIGINT DEFAULT 0,
                    seconds BIGINT CHECK (seconds >= 0 AND seconds < 86400) DEFAULT 0,
                    price DECIMAL(10, 2) DEFAULT 0.00,
                    paid_eur BIGINT DEFAULT 0,
                    paid_cents TINYINT(2) DEFAULT 0 CHECK (paid_cents >= 0 AND paid_cents < 100),
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id))"""
            cursor.execute(create_users_table)
            cursor.execute(create_projects_table)
            cursor.execute(create_stages_table)
            cursor.close()
            self.mysql.commit()
