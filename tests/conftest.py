import pytest
from setup import create_app
from classes.database.databaseinterface import DatabaseInterface


@pytest.fixture()
def app():
    app = create_app("sqlite://")
    return app
