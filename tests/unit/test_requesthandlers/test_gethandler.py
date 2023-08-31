
from datetime import datetime

from pytz import UTC


class TestGetHAndler:

    def test_fetch_user(self, get_handler, new_user):
        user = get_handler.fetch_user(new_user.id)
        assert user.id == new_user.id
        assert user.name == new_user.name
        assert user.email == new_user.email
        assert user.password != new_user.password
        assert user.check_password(new_user.password) is True


    def test_get_projects(self, get_handler, new_user):
        projects = get_handler.get_projects(new_user)
        assert len(projects) == 2
        assert isinstance(projects, list) is True
        assert isinstance(projects[0], dict) is True
        assert projects[0]['id'] == 1
        assert projects[0]['name'] == 'test_name'
        assert projects[0]['owner_id'] == 1
        assert projects[1]['id'] == 2
        assert projects[1]['name'] == 'test_name2'
        assert projects[1]['owner_id'] == 1

    def test_get_project(self, get_handler, new_user):
        project = get_handler.get_project(1, new_user)
        assert project['id']== 1
        assert project['name'] == 'test_name'
        assert project['owner_id'] == 1

    def test_get_stages(self, get_handler, new_user):
        stages = get_handler.get_stages(1, new_user)
        assert len(stages) == 2
        assert isinstance(stages, list) is True
        assert isinstance(stages[0], dict) is True
        assert stages[0]['id'] == 1
        assert stages[0]['name'] == 'test_name'
        assert stages[0]['project_id'] == 1
        assert stages[0]['last_updated'] == datetime(2020, 1, 1, 0, 0, 0, 0)
        assert stages[1]['id'] == 2
        assert stages[1]['name'] == 'test_name2'
        assert stages[1]['project_id'] == 1
        assert stages[1]['last_updated'] == datetime(2020, 1, 1, 0, 0, 0, 0)

    def test_get_stage(self, get_handler, new_user):    
        stage = get_handler.get_stage(1, 1, new_user)
        assert stage['id'] == 1
        assert stage['name'] == 'test_name'
        assert stage['project_id'] == 1
        assert stage['price'] == 1.5
        assert stage['days'] == 1
        assert stage['seconds'] == 1
        assert stage['last_updated'] == datetime(2020, 1, 1, 0, 0, 0, 0)

    