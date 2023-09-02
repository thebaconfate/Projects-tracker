import os
import mysql.connector


class DatabaseInterface():

    def __enter__(self):
        print('opening connection')
        self.mysql = mysql.connector.connect(
            host=os.getenv('MYSQLHOST'),
            user=os.getenv('MYSQLUSER'),
            password=os.getenv('MYSQLPASSWORD'),
            database=os.getenv('MYSQLDATABASE'),
            port=os.getenv('MYSQLPORT')
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('closing connection')
        self.mysql.close()

    def __cursor(self):
        return self.mysql.cursor()

    '''ALL INSERT QUERIES'''

    def insert_user(self, name, email, password):
        self.__cursor().execute(
            '''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (name, email, password))
        self.mysql.commit()

    def insert_project(self, project_name, user_id):
        self.__cursor().execute(
            '''INSERT INTO projects (name, owner_id) VALUES (%s, %s)''', (project_name, user_id))
        self.mysql.commit()

    def insert_stage(self, stage_name, project_id, days, seconds, price, last_updated):
        self.__cursor().execute('''INSERT INTO stages (name, project_id, days, seconds, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)''',
                                (stage_name, project_id, days, seconds, price, last_updated))
        self.mysql.commit()

    '''ALL SELECT QUERIES'''

    def get_projects(self, user_id):
        cursor = self.__cursor()
        cursor.execute(
            '''SELECT id, name FROM projects where owner_id = %s;''', (user_id,))
        projects = cursor.fetchall()
        return projects

    def get_project(self, project_id, user_id):
        cursor = self.__cursor()
        cursor.execute(
            '''SELECT id, name FROM projects where owner_id = %s AND id = %s;''', (user_id, project_id))
        project = cursor.fetchone()
        return project

    def get_project_by_name(self, project_name, user_id):
        cursor = self.__cursor()
        cursor.execute(
            '''SELECT id FROM projects where owner_id = %s AND name = %s;''', (user_id, project_name))
        project = cursor.fetchone()
        return project

    def get_user(self, user_id):
        cursor = self.__cursor()
        cursor.execute(
            '''SELECT id, name, email, password FROM users WHERE id = %s''', (user_id,))
        user = cursor.fetchone()
        return user

    def get_user_by_mail(self, email):
        print('getting user by mail')
        cursor = self.__cursor()
        cursor.execute(
            '''SELECT id, name, email, password FROM users WHERE email = %s''', (email,))
        user = cursor.fetchone()
        return user

    def get_stages(self, project_id, user_id):
        cursor = self.__cursor()
        cursor.execute('''SELECT stages.id, stages.name, project_id, last_updated FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE projects.id = %s AND users.id = %s ORDER BY stages.id ASC;''', (project_id, user_id))
        stages = cursor.fetchall()
        return stages

    def get_stage(self, stage_id, project_id, user_id):
        cursor = self.__cursor()
        cursor.execute('''SELECT stages.id, stages.name, project_id, days, seconds, price, last_updated  FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE stages.id = %s AND projects.id = %s and users.id = %s ;''', (stage_id, project_id, user_id))
        stage = cursor.fetchone()
        return stage

    def get_stage_by_name(self, stage_name, project_id, user_id):
        cursor = self.__cursor()
        cursor.execute('''SELECT stages.id FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE stages.name = %s AND projects.id = %s and users.id = %s ;''', (stage_name, project_id, user_id))
        stage = cursor.fetchone()
        return stage

    '''ALL UPDATE QUERIES'''

    '''UPDATE USER'''

    def update_user_name(self, user_id, new_name):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE users SET name = %s WHERE id = %s''', (new_name, user_id))
        self.mysql.commit()

    def update_user_email(self, user_id, new_email):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE users SET email = %s WHERE id = %s''', (new_email, user_id))
        self.mysql.commit()

    def update_user_password(self, user_id, new_password):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE users SET password = %s WHERE id = %s''', (new_password, user_id))
        self.mysql.commit()

    '''UPDATE PROJECT'''

    def update_project_name(self, project_id, new_name):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE projects SET name = %s WHERE id = %s''', (new_name, project_id))
        self.mysql.commit()

    '''UPDATE STAGE'''

    def update_stage_name(self, stage_id, new_name):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE stages SET name = %s WHERE id = %s''', (new_name, stage_id))
        self.mysql.commit()

    def update_stage_days(self, stage_id, new_days):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE stages SET days = %s WHERE id = %s''', (new_days, stage_id))
        self.mysql.commit()

    def update_stage_seconds(self, stage_id, new_seconds):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE stages SET seconds = %s WHERE id = %s''', (new_seconds, stage_id))
        self.mysql.commit()

    def update_stage_price(self, stage_id, new_price):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE stages SET price = %s WHERE id = %s''', (new_price, stage_id))
        print(f'updated stage price {new_price} {stage_id}')
        self.mysql.commit()

    def update_stage_last_updated(self, stage_id, new_last_updated):
        cursor = self.__cursor()
        cursor.execute(
            '''UPDATE stages SET last_updated = %s WHERE id = %s''', (new_last_updated, stage_id))
        self.mysql.commit()

    '''ALL DELETE QUERIES'''

    def delete_user(self, user_id):
        cursor = self.__cursor()
        cursor.execute('''DELETE FROM users WHERE id = %s''', (user_id,))
        self.mysql.commit()

    def delete_project(self, project_id):
        cursor = self.__cursor()
        cursor.execute('''DELETE FROM projects WHERE id = %s''', (project_id,))
        self.mysql.commit()

    def delete_stage(self, stage_id):
        cursor = self.__cursor()
        cursor.execute('''DELETE FROM stages WHERE id = %s''', (stage_id,))
        self.mysql.commit()
