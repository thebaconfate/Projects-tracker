from flask import Blueprint, jsonify, make_response, request
from flask_login import login_required, current_user
from src.classes.requestshandlers.gethandler import GetHandler
from src.classes.requestshandlers.delhandler import Delhandler
from src.classes.requestshandlers.inithandler import Inithandler
from src.classes.requestshandlers.puthandler import Puthandler
from src.classes.requestshandlers.posthandler import Posthandler
from src.classes.errorhandler import ErrorHandler
from src.setup import login_manager, tz

bp = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    handler = GetHandler()
    return handler.fetch_user(user_id)

# * error handler for error codes.


@bp.errorhandler(Exception)
def internal_server_error(e):
    return ErrorHandler().handle(e)


@bp.errorhandler(500)
def internal_server_error_500(e):
    return make_response(jsonify({
        'msg': 'unknown internal server error'
    }), 500)


@bp.route('/')
def index():
    return jsonify({'msg': 'hello world'}), 200


@bp.post('/register', strict_slashes=False)
def register():
    handler = Posthandler()
    handler.register(request.json)
    return jsonify('added user'), 200


@bp.post('/login/', strict_slashes=False)
def login():
    handler = Posthandler()
    result = handler.login(request.json)
    return jsonify(result), 200


@bp.route('/logout/', strict_slashes=False)
@login_required
def logout():
    handler = Posthandler()
    handler.logout()
    return jsonify({"msg": "logged user out"}), 200


@bp.post('/create_project')
@login_required
def create_project():
    # * adds a project to the database
    handler = Posthandler()
    handler.create_project(request.json, current_user)
    return jsonify('added project'), 200


# * gets all projects names and ids from the database.
@bp.get('/projects:all')
@login_required
def get_projects():
    handler = GetHandler()
    results = handler.get_projects(current_user)
    return results, 200


# * gets all stages from a project
@bp.get('/project:<project_id>/stages:all')
@login_required
def get_stages(project_id):
    handler = GetHandler()
    result = handler.get_stages(project_id, current_user)
    return result, 200


@bp.post('/project:<project_id>/create_stage')
@login_required
def create_stage(project_id):
    handler = Posthandler()
    handler.create_stage(request.json, project_id, current_user)
    return jsonify('stage_added'), 200


@bp.route('/project:<project_id>/stage:<stage_id>', methods=['GET', 'PUT'])
@login_required
def get_stage(project_id, stage_id):
    # * gets information about a stage from a project
    if request.method == 'GET':
        handler = GetHandler()
        result = handler.get_stage(project_id, stage_id, current_user)
        return result, 200
    elif request.method == 'PUT':
        handler = Puthandler()
        result = handler.update_stage(
            project_id, stage_id, request.json, current_user)
        return result, 200


@bp.put('/project:<project_id>/stage:<stage_id>/add')
@login_required
def add_time(project_id, stage_id):
    handler = Puthandler()
    handler.add_time(project_id, stage_id, request.json, current_user)
    return jsonify('time added'), 200


@bp.put('/project:<project_id>')
@login_required
def update_project(project_id):
    handler = Puthandler()
    handler.update_project(project_id, request.json, current_user)
    return 'project updated', 200


@bp.delete('/project:<project_id>/stage:<stage_id>')
@login_required
def delete_stage(project_id, stage_id):
    # TODO handler.delete_stage(project_id, stage_id)
    # TODO implement this method. It should delete the stage from the database.
    return 'stage deleted', 200


@bp.delete('/project:<project_id>')
@login_required
def delete_project(project_id):
    # TODO handler.delete_project(project_id)
    # TODO implement this method. It should delete the project from the database.
    return 'project deleted', 200


# TODO Add user authentication and authorization so only an admin can migrate projects and stages.
# TODO Add user authentication so each user can only create edit and remove their own projects and stages.
