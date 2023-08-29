from setup import db


class DatabaseInterface():

    def __init__(self):
        self.db = db

    '''ALL INSERT QUERIES'''

    def insert_user(self, name, email, password):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (name, email, password))
        self.db.connection.commit()
        cursor.close()

    def insert_project(self, project_name, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''INSERT INTO projects (name, owner_id) VALUES (%s, %s)''', (project_name, user_id))
        self.db.connection.commit()
        cursor.close()

    def insert_stage(self, stage_name, project_id, days, seconds, price, last_updated):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''INSERT INTO stages (stage_name, project_id, days, seconds, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)''', (stage_name, project_id, days, seconds, price, last_updated))
        self.db.connection.commit()
        cursor.close()

    '''ALL SELECT QUERIES'''

    def get_projects(self, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT id, name FROM projects where owner_id = %s;
        ''', (user_id,))
        projects = cursor.fetchall()
        cursor.close()
        return projects

    def get_project(self, project_id, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''
            SELECT id, name FROM projects where owner_id = %s AND id = %s;
        ''', (user_id, project_id))
        project = cursor.fetchone()
        cursor.close()
        return project

    def get_user(self, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT id, name, email, password FROM users WHERE id = %s''', (user_id,))
        user = cursor.fetchone()
        cursor.close()
        return user

    def get_stages(self, project_id, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''SELECT stages.id, project_id, stage_name, last_updated FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE projects.id = %s AND users.id = %s ORDER BY stages.id ASC;''', (project_id, user_id))
        stages = cursor.fetchall()
        cursor.close()
        return stages

    def get_stage(self, stage_id, project_id, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''SELECT stages.id, stage_name, project_id, days, seconds, price, last_updated  FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE stages.id = %s AND projects.id = %s and users.id = %s ;''', (stage_id, project_id, user_id))
        stage = cursor.fetchone()
        cursor.close()
        return stage

    '''ALL UPDATE QUERIES'''

    '''UPDATE USER'''

    def update_user_name(self, user_id, new_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE users SET name = %s WHERE id = %s''', (new_name, user_id))
        self.db.connection.commit()
        cursor.close()

    def update_user_email(self, user_id, new_email):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE users SET email = %s WHERE id = %s''', (new_email, user_id))
        self.db.connection.commit()
        cursor.close()

    def update_user_password(self, user_id, new_password):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE users SET password = %s WHERE id = %s''', (new_password, user_id))
        self.db.connection.commit()
        cursor.close()

    '''UPDATE PROJECT'''

    def update_project_name(self, project_id, new_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE projects SET name = %s WHERE id = %s''', (new_name, project_id))
        self.db.connection.commit()
        cursor.close()

    '''UPDATE STAGE'''

    def update_stage_name(self, stage_id, new_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE stages SET stage_name = %s WHERE id = %s''', (new_name, stage_id))
        self.db.connection.commit()
        cursor.close()

    def update_stage_days(self, stage_id, new_days):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE stages SET days = %s WHERE id = %s''', (new_days, stage_id))
        self.db.connection.commit()
        cursor.close()

    def update_stage_seconds(self, stage_id, new_seconds):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE stages SET seconds = %s WHERE id = %s''', (new_seconds, stage_id))
        self.db.connection.commit()
        cursor.close()

    def update_stage_price(self, stage_id, new_price):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE stages SET price = %s WHERE id = %s''', (new_price, stage_id))
        self.db.connection.commit()
        cursor.close()

    def update_stage_last_updated(self, stage_id, new_last_updated):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''UPDATE stages SET last_updated = %s WHERE id = %s''', (new_last_updated, stage_id))
        self.db.connection.commit()
        cursor.close()

    '''ALL DELETE QUERIES'''

    def delete_user(self, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = %s''', (user_id,))
        self.db.connection.commit()
        cursor.close()

    def delete_project(self, project_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''DELETE FROM projects WHERE id = %s''', (project_id,))
        self.db.connection.commit()
        cursor.close()

    def delete_user(self, stage_id):
        cursor = self.db.connection.cursor()
        cursor.execute('''DELETE FROM stages WHERE id = %s''', (stage_id,))
        self.db.connection.commit()
        cursor.close()
