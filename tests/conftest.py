import pytest 
from setup import create_app

@pytest.fixture()
def app():
    app = create_app("sqlite://")
    return app