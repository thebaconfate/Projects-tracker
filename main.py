from datetime import datetime
from pytz import timezone, utc
import os
from dotenv import load_dotenv
from flask import Flask, abort, jsonify, make_response, request
from src.classes.errorhandler import ErrorHandler
from src.classes.customerrors.customerror import CustomError
from src.classes.customerrors.inputerror import InputException
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

handler = Requesthandler(db)

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


# * gets all projects names and ids from the database.
@app.get('/projects')
def get_projects():
    results = handler.get_projects()
    return results, 200


# * gets all stages from a project
@app.get('/<project_name>/')
def get_stages(project_name):
    result = handler.get_stages(project_name)
    return result, 200


# * gets information about a stage from a project
@app.get('/<project_name>/<stage_name>')
def get_project(project_name, stage_name):
    result = handler.get_stage(project_name, stage_name)
    return result, 200


# * migrates stage(s) from a json file to the database. Also adds the project if it doesn't exist.
@app.post('/migrate/<project_name>')
def migrate_stages(project_name):
    handler.migrate_stages(project_name, request.json)
    return 'migration successful', 200


# * migrates all projects and stages from a json file to the database.
@app.post('/migrate')
def migrate_projects():
    handler.migrate_projects(request.json)
    return 'migration successful', 200


# TODO Implement a route that allows the user to add a project to the database.
# TODO Implement a route that allows the user to add a stage to a project in the database.
# TODO Implement a route that allows the user to rename a stage in the database.
# TODO Implement a route that allows the user to update a price of a stage in the database
# TODO implement a route that allows the user to update the days & hours spent on a stage. This should automatically update the last update value of the stage.
# TODO Implement a route that allows the user to delete a stage from the database.
# TODO Implement a route that allows the user to delete a project from the database.
# TODO Implement a route that allows the user to rename a project in the database.

# TODO Add user authentication and authorization so only an admin can migrate projects and stages.
# TODO Add user authentication so each user can only create edit and remove their own projects and stages.

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=testing)
