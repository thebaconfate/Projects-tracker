from datetime import datetime
from pytz import timezone, utc
import os
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, make_response, request
from src.classes.requesthandler import Requesthandler
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
db = MySQL(app)
handler = Requesthandler(db=db)


@app.errorhandler(500)
def internal_error(error):
    return os.getenv('ERROR_500_MSG'), 500


@app.get('/init_tables')
def init_tables():
    handler.init_tables()
    return 'done', 200

# * gets all projects


@app.get('/projects')
def get_projects():
    results = handler.get_projects()
    return results, 200

# * gets all stages from a project


@app.get('/<project_name>/')
def get_stages(project_name):
    result = handler.get_stages(project_name)
    return result, 200

# * gets information about a stage


@app.get('/<project_name>/<stage_name>')
def get_project(project_name, stage_name):
    result = handler.get_stage(project_name, stage_name)
    return result

# * migrates stage(s) from a json file to the database. Also adds the project if it doesn't exist.


@app.post('/migrate/<project_name>')
def migrate_stages(project_name):

    # TODO refactor this

    stages = request.json
    cursor = db.connection.cursor()
    cursor.execute(
        f'''INSERT INTO PROJECTS (project_name) SELECT ("{project_name}") WHERE NOT EXISTS (SELECT project_id FROM projects WHERE project_name = "{project_name}")''')
    db.connection.commit()
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
        db.connection.commit()

    cursor.close()
    return 'migration succesfull', 200
# * migrates all projects and stages from a json file to the database.


@app.post('/migrate')
def migrate_projects():
    # TODO implement this
    pass


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=testing)
