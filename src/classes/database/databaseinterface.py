import os
import mysql.connector  


class DatabaseInterface():

    def connect(self):
        db = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB_TEST')
        )
        return db, db.cursor()

    def disconnect(self, mysql):
        mysql.close()

    '''ALL INSERT QUERIES'''

    def insert_user(self, name, email, password):
        mysql, cursor = self.connect()
        cursor.execute(
            '''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (name, email, password))
        mysql.commit()
        self.disconnect(mysql)

    def insert_project(self, project_name, user_id):
        mysql, cursor = self.connect()
        cursor.execute(
            '''INSERT INTO projects (name, owner_id) VALUES (%s, %s)''', (project_name, user_id))
        mysql.commit()
        self.disconnect(mysql)

    def insert_stage(self, stage_name, project_id, days, seconds, price, last_updated):
        mysql, cursor = self.connect()
        cursor.execute(
            '''INSERT INTO stages (stage_name, project_id, days, seconds, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)''', (stage_name, project_id, days, seconds, price, last_updated))
        mysql.commit()
        self.disconnect(mysql)

    '''ALL SELECT QUERIES'''

    def get_projects(self, user_id):
        mysql, cursor = self.connect()
        cursor.execute('''
            SELECT id, name FROM projects where owner_id = %s;
        ''', (user_id,))
        projects = cursor.fetchall()
        self.disconnect(mysql)
        return projects

    def get_project(self, project_id, user_id):
        mysql, cursor = self.connect()
        cursor.execute('''
            SELECT id, name FROM projects where owner_id = %s AND id = %s;
        ''', (user_id, project_id))
        project = cursor.fetchone()
        self.disconnect(mysql)
        return project

    def get_project_by_name(self, project_name, user_id):
        mysql, cursor = self.connect()
        cursor.execute('''
            SELECT id FROM projects where owner_id = %s AND name = %s;
        ''', (user_id, project_name))
        project = cursor.fetchone()
        self.disconnect(mysql)
        return project

    def get_user(self, user_id):
        mysql, cursor = self.connect()
        cursor.execute(
            '''SELECT id, name, email, password FROM users WHERE id = %s''', (user_id,))
        user = cursor.fetchone()
        self.disconnect(mysql)
        return user

    def get_user_by_mail(self, email):
        mysql, cursor = self.connect()
        cursor = mysql.cursor()
        cursor.execute(
            '''SELECT id, name, email, password FROM users WHERE email = %s''', (email,))
        user = cursor.fetchone()
        self.disconnect(mysql)
        return user

    def get_stages(self, project_id, user_id):
        mysql, cursor = self.connect()
        cursor.execute('''SELECT stages.id, stage_name, project_id, last_updated FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE projects.id = %s AND users.id = %s ORDER BY stages.id ASC;''', (project_id, user_id))
        stages = cursor.fetchall()
        self.disconnect(mysql)
        return stages

    def get_stage(self, stage_id, project_id, user_id):
        mysql, cursor = self.connect()
        cursor.execute('''SELECT stages.id, stage_name, project_id, days, seconds, price, last_updated  FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE stages.id = %s AND projects.id = %s and users.id = %s ;''', (stage_id, project_id, user_id))
        stage = cursor.fetchone()
        self.disconnect(mysql)
        return stage

    def get_stage_by_name(self, stage_name, project_id, user_id):
        mysql, cursor = self.connect()
        cursor.execute('''SELECT stages.id FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE stage_name = %s AND projects.id = %s and users.id = %s ;''', (stage_name, project_id, user_id))
        stage = cursor.fetchone()
        self.disconnect(mysql)
        return stage

    '''ALL UPDATE QUERIES'''

    '''UPDATE USER'''

    def update_user_name(self, user_id, new_name):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE users SET name = %s WHERE id = %s''', (new_name, user_id))
        mysql.commit()
        self.disconnect(mysql)

    def update_user_email(self, user_id, new_email):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE users SET email = %s WHERE id = %s''', (new_email, user_id))
        mysql.commit()
        self.disconnect(mysql)

    def update_user_password(self, user_id, new_password):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE users SET password = %s WHERE id = %s''', (new_password, user_id))
        mysql.commit()
        self.disconnect(mysql)

    '''UPDATE PROJECT'''

    def update_project_name(self, project_id, new_name):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE projects SET name = %s WHERE id = %s''', (new_name, project_id))
        mysql.commit()
        self.disconnect(mysql)

    '''UPDATE STAGE'''

    def update_stage_name(self, stage_id, new_name):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE stages SET stage_name = %s WHERE id = %s''', (new_name, stage_id))
        mysql.commit()
        self.disconnect(mysql)

    def update_stage_days(self, stage_id, new_days):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE stages SET days = %s WHERE id = %s''', (new_days, stage_id))
        mysql.commit()
        self.disconnect(mysql)

    def update_stage_seconds(self, stage_id, new_seconds):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE stages SET seconds = %s WHERE id = %s''', (new_seconds, stage_id))
        mysql.commit()
        self.disconnect(mysql)

    def update_stage_price(self, stage_id, new_price):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE stages SET price = %s WHERE id = %s''', (new_price, stage_id))
        mysql.commit()
        self.disconnect(mysql)

    def update_stage_last_updated(self, stage_id, new_last_updated):
        mysql, cursor = self.connect()
        cursor.execute(
            '''UPDATE stages SET last_updated = %s WHERE id = %s''', (new_last_updated, stage_id))
        mysql.commit()
        self.disconnect(mysql)

    '''ALL DELETE QUERIES'''

    def delete_user(self, user_id):
        mysql, cursor = self.connect()
        cursor.execute('''DELETE FROM users WHERE id = %s''', (user_id,))
        mysql.commit()
        self.disconnect(mysql)

    def delete_project(self, project_id):
        mysql, cursor = self.connect()
        cursor.execute('''DELETE FROM projects WHERE id = %s''', (project_id,))
        mysql.commit()
        self.disconnect(mysql)

    def delete_stage(self, stage_id):
        mysql, cursor = self.connect()
        cursor.execute('''DELETE FROM stages WHERE id = %s''', (stage_id,))
        mysql.commit()
        self.disconnect(mysql)
