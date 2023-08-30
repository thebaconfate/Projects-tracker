from datetime import datetime
from unittest.mock import MagicMock, Mock
import pytest
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
from src.classes.requesthandler import Requesthandler


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
    user = User(id=1, name='test_name', email='test_email@email.com',
                password='test_password')
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
def mock_db():
    return Mock()


@pytest.fixture()
def db_interface(mock_db):
    return DatabaseInterface(mock_db)


# ! Might have to refactor this mocking the return values from method calls in the db_interface
@pytest.fixture()
def delhandler(db_interface):
    return Delhandler(db_interface)


@pytest.fixture()
def gethandler(db_interface):
    return GetHandler(db_interface)

@pytest.fixture()
def inithandler(db_interface):
    return Inithandler(db_interface)

@pytest.fixture()
def posthandler(db_interface):
    return Posthandler(db_interface)

@pytest.fixture()
def puthandler(db_interface):
    return Puthandler(db_interface)

@pytest.fixture()
def requesthandler(db_interface):
    return Requesthandler(db_interface)     