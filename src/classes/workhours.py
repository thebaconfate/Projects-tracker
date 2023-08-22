
import sys
from pytz import timezone
from src.classes.errors import Errors
from src.classes.success import Success


class Workhours:

    def __init__(self, mysql):
        self.__timezone = timezone('Europe/Brussels')
        self.__mysql = mysql

    def init_tables(self):
        try:
            cursor = self.__mysql.connection.cursor()
            create_projects = "CREATE_ TABLE IF NOT EXISTS projects (project_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, project_name VARCHAR(255) NOT NULL);"
            cursor.execute(create_projects)
            create_stages = "CREATE TABLE IF NOT EXISTS stages (stage_name VARCHAR(255) PRIMARY KEY NOT NULL, project_id INT NOT NULL, days INT NOT NULL, seconds INT NOT NULL, stage_price INT NOT NULL, last_updated TIMESTAMP NOT NULL, FOREIGN KEY (project_id) REFERENCES projects(project_id));"
            cursor.execute(create_stages)
            self.__mysql.connection.commit()
            cursor.close()
        except Exception:
            cursor.close()
            error = 'Method: ' + sys._getframe().f_code.co_name.__str__() + ' in Class: ' + self.__class__.__name__.__str__()
            return Errors("Caught exception", error , "Something went wrong while initializing the tables.")
        else:
            return Success("Ok", 'Tables were already initialized or were created successfully.')
        
        

