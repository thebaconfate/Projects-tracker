from datetime import datetime, timedelta
import sys
from pytz import timezone, utc
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from src.classes.errors import Errors
from src.classes.workhours import Workhours
import src.workhours as wh
import src.workhoursdecoder as dec
import src.workhoursencoder as enc
from flask_mysqldb import MySQL

testing = True
if testing:
    filename = 'files/test_workhours.json'
else:
    filename = 'files/workhours.json'

app = Flask(__name__)
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv(
    'MYSQL_DB_TEST') if testing else os.getenv('MYSQL_DB')
mysql = MySQL(app)
workhours = Workhours(mysql)


@app.get('/init_tables')
def init_tables():
    return workhours.init_tables().get_report()


@app.route('/projects')
def get_projects():
    query = "SELECT project_id, project_name FROM projects"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    headers = cursor.description
    rows = cursor.fetchall()
    results = []
    for i in range(0, len(rows)):
        results.append({
            "project_id": rows[i][0],
            "project_name": rows[i][1]
        })
    results = {"projects": results}
    cursor.close()
    return results


@app.route('/<project_name>/stages')
def get_stages(project_name):
    query = f'SELECT stage_name FROM stages where project_id = (SELECT project_id FROM projects where project_name = {project_name})'
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    headers = cursor.description
    rows = cursor.fetchall()
    results = [rows]
    """ for i in range(0, len(rows)):
        results.append({
            "project_id": rows[i][0],
            "project_name": rows[i][1]
        }) """
    results = {"projects": results}
    cursor.close()
    return results


@app.get('/<project_name>')
def get_project(project_name):
    query = f"SELECT Projects.project_name, Stages.stage_name, Stages.days, Stages.seconds, stages.stage_price from projects right join stages on projects.project_id = stages.project_id where Projects.project_name = '{project_name}'"
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    headers = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    results = {}
    print(f'{headers}\n')
    print(rows)
    for i in range(0, len(rows)):
        results[rows[i][1]] = {
            "time": {
                headers[2]: rows[i][2],
                headers[3]: rows[i][3]
            },
            headers[4]: rows[i][4]
        }
    cursor.close()
    return results


@app.post('/migrate/<project_name>')
def migrate_project(project_name):
    stages = request.json
    cursor = mysql.connection.cursor()
    cursor.execute(
        f'''INSERT INTO PROJECTS (project_name) SELECT ("{project_name}") WHERE NOT EXISTS (SELECT project_id FROM projects WHERE project_name = "{project_name}")''')
    mysql.connection.commit()
    project_id = cursor.execute(
        f"SELECT project_id FROM projects WHERE project_name = '{project_name}'")
    for stage, stage_property in stages.items():
        print(stage_property)
        timestamp = datetime.strptime(
            stage_property['last_updated'], '%d-%m-%YT%H:%M:%S%z').replace(tzinfo=timezone('Europe/Brussels'))
        timestamp = timestamp.astimezone(utc)
        query = f'''INSERT INTO stages (stage_name, project_id, days, seconds, stage_price, last_updated) SELECT 
            "{stage}",
            {project_id},
            {stage_property['time']['days']},
            {stage_property['time']['seconds']},
            {stage_property['price']},
            "{timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            WHERE NOT EXISTS (
                SELECT stage_name FROM stages WHERE stage_name = "{stage}" AND project_id = {project_id}
                );'''
        print(query)
        cursor.execute(query)
        mysql.connection.commit()

    cursor.close()
    return 'migration succesfull', 200


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=testing)
