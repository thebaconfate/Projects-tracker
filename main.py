import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, make_response, request
from flask_mysqldb import MySQL
from pytz import timezone, utc

from src.classes.customerrors.customerror import CustomError
from src.classes.customerrors.inputerror import InputException
from src.classes.errorhandler import ErrorHandler
from src.classes.requesthandler import Requesthandler

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

handler = Requesthandler(db, timezone('Europe/Brussels'))

# * error handler for thrown exceptions.


@app.errorhandler(Exception)
def internal_server_error(e):
    return ErrorHandler().handle(e)

# * error handler for error codes.


@app.errorhandler(500)
def internal_server_error_500(e):
    return make_response(jsonify({
        'msg': 'unknown internal server error'
    }), 500)


# * creates the required tables in the database.
@app.get('/init_tables')
def init_tables():
    print('init tables')
    handler.init_tables()
    return 'done', 200

# * migrates stage(s) from a json file to the database. Also adds the project if it doesn't exist.


@app.post('/migrate/project:<project_name>')
def migrate_stages(project_name):
    handler.migrate_stages(project_name, request.json)
    return 'migration successful', 200


# * migrates all projects and stages from a json file to the database.
@app.post('/migrate/projects')
def migrate_projects():
    handler.migrate_projects(request.json)
    return 'migration successful', 200

# * gets all projects names and ids from the database.


@app.get('/projects:all')
def get_projects():
    # TODO add user_id to the request
    results = handler.get_projects()
    return results, 200


# * gets all stages from a project
@app.get('/project:<project_id>/stages:all')
def get_stages(project_id):
    result = handler.get_project(project_id)
    return result, 200


# * gets information about a stage from a project
@app.route('/project:<project_id>/stage:<stage_id>', methods=['GET'])
def get_project(project_id, stage_id):
    if request.method == 'GET':
        result = handler.get_stage(project_id, stage_id)
        return result, 200


# * adds a project to the database
@app.post('/create_project')
def create_project():
    handler.create_project(request.json)
    return 'project added', 200


@app.post('/project:<project_id>/create_stage')
def create_stage(project_id):
    handler.create_stage(project_id, request.json)
    return 'stage added', 200


@app.put('/project:<project_id>/stage:<stage_id>')
def update_stage(project_id, stage_id):
    # TODO handler.update_stage(project_id, stage_id, request.json)
    # TODO implement this method. It should take a json and update all listed properties.
    # TODO Implement a route that allows the user to rename a stage in the database.
    # TODO Implement a route that allows the user to update a price of a stage in the database
    # TODO implement a route that allows the user to update the days & hours spent on a stage. This should automatically update the last update value of the stage.
    return 'stage updated', 200


@app.put('/project:<project_id>')
def update_project(project_id):
    # TODO handler.update_project(project_id, request.json)
    # TODO implement this method. It should take a json and rename the project.
    return 'project updated', 200


@app.delete('/project:<project_id>/stage:<stage_id>')
def delete_stage(project_id, stage_id):
    # TODO handler.delete_stage(project_id, stage_id)
    # TODO implement this method. It should delete the stage from the database.
    return 'stage deleted', 200


@app.delete('/project:<project_id>')
def delete_project(project_id):
    # TODO handler.delete_project(project_id)
    # TODO implement this method. It should delete the project from the database.
    return 'project deleted', 200


# TODO Add user authentication and authorization so only an admin can migrate projects and stages.
# TODO Add user authentication so each user can only create edit and remove their own projects and stages.
if __name__ == "__main__":
    load_dotenv()
    app.run(debug=testing)
