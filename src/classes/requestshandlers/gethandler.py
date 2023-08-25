
''' class to delegate requests that fetch data to.'''


class GetHandler():

    def __init__(self, db):
        self.db = db

    def get_projects(self):
        cursor = self.db.connection.cursor()
        query = "SELECT * FROM projects"
        cursor.execute(query)
        projects = cursor.fetchall()
        cursor.close()
        results = []
        for i in range(0, len(projects)):
            results.append({
                "project_id": projects[i][0],
                "project_name": projects[i][1]
            })
        return results

    def get_project(self, project_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT * from projects where project_name = %s''', (project_name,))
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            result = {
                "project_id": row[0],
                "project_name": row[1]
            }
        return result

    def get_stages(self, project_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT stage_id, stage_name FROM stages where project_id = (SELECT id FROM projects where project_name = %s)''', (project_name,))
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            result.append({
                "stage_id": row[0],
                "stage_name": row[1]
            })
        return result

    def get_stage(self, project_name, stage_name):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT * from stages where stage_name = %s and project_id = (SELECT id FROM projects where project_name = %s)''', (stage_name, project_name))
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            result = {
                "stage_id": row[0],
                "stage_name": row[1],
                "project_id": row[2],
                "days": row[3],
                "seconds": row[4],
                "stage_price": row[5],
                "last_updated": row[6]
            }
        return result
