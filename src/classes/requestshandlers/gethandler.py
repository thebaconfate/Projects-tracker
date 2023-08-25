
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

    def get_project(self, project_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT id, stage_name from stages where project_id = %s''', (project_id,))
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "stage_name": row[1]
            })
        return result

    # * get all stages from a user
    # ! this function is currently not in use
    def get_stages(self, project_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT id, project_id, stage_name FROM stages where project_id = id''', (project_id,))
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            result.append({
                "stage_id": row[0],
                "project_id": row[1],
                "stage_name": row[2]
            })
        return result

    def get_stage(self, project_id, stage_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            '''SELECT * from stages where id = %s and project_id = %s''', (stage_id, project_id))
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            result.append({
                "stage_id": row[0],
                "stage_name": row[1],
                "project_id": row[2],
                "time": {
                    "days": row[3],
                    "seconds": row[4]
                },
                "price": row[5],
                "last_updated": row[6]
            })
        return result
