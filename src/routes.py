from typing import Annotated
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from src.classes.users.usermodels import UserRegister, UserLogin, UserLogout
from src.setup import oauth2_scheme

app = FastAPI()


@app.get("/")
async def index():
    return {"msg": "hello world"}


@app.post("/user/register")
async def register_user(user_register: UserRegister):

    return ("msg": "Added user")


"""
@app.route("/")
def index():
    return jsonify({"msg": "hello world"}), 200


@bp.post("/register", strict_slashes=False)
def register():
    handler = Posthandler()
    handler.register(request.args)
    return jsonify("added user"), 200


@bp.post("/login", strict_slashes=False)
def login():
    handler = Posthandler()
    result = handler.login(request.args)
    return jsonify(result), 200


@bp.route("/logout/", strict_slashes=False)
@login_required
def logout():
    handler = Posthandler()
    handler.logout()
    return jsonify({"msg": "logged user out"}), 200


@bp.post("/create_project")
@login_required
def create_project():
    handler = Posthandler()
    handler.create_project(request.args, current_user)
    return jsonify("added project"), 200


# * gets all projects names and ids from the database.
@bp.get("/projects:all")
@login_required
def get_projects():
    handler = GetHandler()
    results = handler.get_projects(current_user)
    return jsonify(results), 200


# * gets all stages from a project
@bp.route("/project", methods=["GET", "PUT"])
@login_required
def project():
    match request.method:
        case "GET":
            handler = GetHandler()
            project_id = request.args.get("project_id")
            result = handler.get_stages(project_id, current_user)
            return jsonify(result), 200
        case "PUT":
            handler = Puthandler()
            project_id = request.args.get(project_id)
            result = handler.update_project(project_id, request.json, current_user)
            return jsonify(result), 200


@bp.route("/stage", methods=["GET", "PUT", "POST"])
@login_required
def stage():
    # * gets information about a stage from a project
    match request.method:
        case "GET":
            handler = GetHandler()
            result = handler.get_stage(request.args, current_user)
            return jsonify(result), 200
        case "PUT":
            handler = Puthandler()
            result = handler.update_stage(request.args, current_user)
            return result, 200
        case "POST":
            handler = Posthandler()
            handler.create_stage(request.args, current_user)
            return "stage created", 200


@bp.put("/time")
@login_required
def add_time():
    handler = Puthandler()
    handler.add_time(request.args, current_user)
    return jsonify("time added"), 200


@bp.get("/calc")
@login_required
def calc_time():
    handler = GetHandler()
    project_id = request.args.get("project_id")
    result = handler.calc(project_id, current_user)
    return jsonify(result), 200


@bp.delete("/project:<project_id>/stage:<stage_id>")
@login_required
def delete_stage(project_id, stage_id):
    # TODO handler.delete_stage(project_id, stage_id)
    # TODO implement this method. It should delete the stage from the database.
    return "stage deleted", 200


@bp.delete("/project:<project_id>")
@login_required
def delete_project(project_id):
    # TODO handler.delete_project(project_id)
    # TODO implement this method. It should delete the project from the database.
    return "project deleted", 200


# TODO Add user authentication and authorization so only an admin can migrate projects and stages.
# TODO Add user authentication so each user can only create edit and remove their own projects and stages.
"""
