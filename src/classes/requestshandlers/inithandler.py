
import sys
from pytz import timezone


class Inithandler():

    def __init__(self, db):
        self.db = db

    def init_tables(self):
        print('init tables')
        cursor = self.db.connection.cursor()
        create_projects = "CREATE TABLE IF NOT EXISTS projects (project_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, project_name VARCHAR(255) NOT NULL);"
        cursor.execute(create_projects)
        create_stages = "CREATE TABLE IF NOT EXISTS stages (stage_name VARCHAR(255) PRIMARY KEY NOT NULL, project_id INT NOT NULL, days INT NOT NULL, seconds INT NOT NULL, stage_price INT NOT NULL, last_updated TIMESTAMP NOT NULL, FOREIGN KEY (project_id) REFERENCES projects(project_id));"
        cursor.execute(create_stages)
        self.db.connection.commit()
        cursor.close()
        print('done')

 
