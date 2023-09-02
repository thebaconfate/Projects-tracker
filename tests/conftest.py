import pytest
from datetime import datetime
from unittest.mock import Mock
from src.classes.requestshandlers.inithandler import Inithandler
from src.classes.requestshandlers.posthandler import Posthandler
from src.classes.requestshandlers.puthandler import Puthandler
from src.classes.requestshandlers.gethandler import GetHandler
from src.classes.requestshandlers.delhandler import Delhandler
from src.classes.models.project import Project
from src.classes.models.stage import Stage
from src.classes.models.user import User
from src import create_app
from src.classes.database.databaseinterface import DatabaseInterface
from src.classes.requesthandler import HandlerFactory
from src.setup import bcrypt


test_user_name = 'test_name'
test_user_email = "test_user@testmail.com"
test_pass = 'test_password'
hashed_test_pass = bcrypt.generate_password_hash(test_pass)


@pytest.fixture()
def app():
    app = create_app({
        'TESTING': True,
    })
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def new_user():
    user = User(id=1, name=test_user_name, email=test_user_email,
                password=test_pass)
    return user


@pytest.fixture()
def new_stage():
    stage = Stage(id=1,
                  name='test_name',
                  project_id=1,
                  price=1.0,
                  days=1,
                  seconds=1,
                  last_updated=datetime(2020, 1, 1, 0, 0, 0, 0))
    return stage


@pytest.fixture()
def new_project():
    project = Project(id=1,
                      name='test_name',
                      owner_id=1)
    return project


@pytest.fixture()
def db_interface():
    return DatabaseInterface()


# ! Might have to refactor this mocking the return values from method calls in the db_interface
@pytest.fixture()
def delhandler(db_interface):
    return Delhandler(db_interface)


@pytest.fixture()
def get_handler():
    db_interface = Mock()
    db_interface.get_user.return_value = (
        1, test_user_name, test_user_email, hashed_test_pass)
    db_interface.get_projects.return_value = (
        (1, 'test_name', 1), (2, 'test_name2', 1))
    db_interface.get_project.return_value = (1, 'test_name', 1)
    db_interface.get_stages.return_value = ((1, 'test_name', 1, datetime(
        2020, 1, 1, 0, 0, 0, 0)), (2, 'test_name2', 1, datetime(2020, 1, 1, 0, 0, 0, 0)))
    db_interface.get_stage.return_value = (
        1, 'test_name', 1, 1.5, 1, 1, datetime(2020, 1, 1, 0, 0, 0, 0))
    return GetHandler(db_interface)


@pytest.fixture()
def inithandler():
    return Inithandler(Mock())


@pytest.fixture()
def posthandler(db_interface):
    return Posthandler(db_interface)


@pytest.fixture()
def puthandler(db_interface):
    return Puthandler(db_interface)


@pytest.fixture()
def requesthandler(db_interface):
    return HandlerFactory(db_interface)
