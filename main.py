import os
from dotenv import load_dotenv
from flask import Flask, jsonify
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
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
mysql = MySQL(app)


@app.route('/')
def index():
    return 'Welcome to the workhours api, where you can fetch, adapt and save data from your projects.'


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


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=testing)
