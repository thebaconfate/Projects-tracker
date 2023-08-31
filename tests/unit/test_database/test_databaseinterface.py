
from unittest import mock
from unittest.mock import Mock

import pytest
time = '2020-01-01 00:00:00'

class TestDataBaseInterface:

    '''INSERT TESTS'''

    def test_insert_user(self, db_interface):
        db_interface.insert_user(
            'test_name', 'test_email', 'test_password')
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''',
            ('test_name', 'test_email', 'test_password'))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_insert_project(self, db_interface):
        db_interface.insert_project('test_project', 1)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''INSERT INTO projects (name, owner_id) VALUES (%s, %s)''',
            ('test_project', 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_insert_stage(self, db_interface):
        db_interface.insert_stage(
            'test_stage', 1, 1, 1, 1.0, time)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''INSERT INTO stages (stage_name, project_id, days, seconds, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)''',
            ('test_stage', 1, 1, 1, 1.0, time))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    '''SELECT TESTS'''    

    def test_get_projects(self, db_interface):
        db_interface.db.connection.cursor().fetchall.return_value = [
            (1, 'test_project'), (2, 'test_project2')]
        projects = db_interface.get_projects(1)
        db_interface.db.connection.cursor().execute.assert_called_once()
        db_interface.db.connection.cursor().fetchall.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
        assert projects == [(1, 'test_project'), (2, 'test_project2')]

    def test_get_project(self, db_interface):
        db_interface.db.connection.cursor().fetchone.return_value = (1, 'test_project')
        project = db_interface.get_project(1, 1)
        db_interface.db.connection.cursor().execute.assert_called_once()
        db_interface.db.connection.cursor().fetchone.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
        assert project == (1, 'test_project')

    def test_get_project_by_name(self, db_interface):
        db_interface.db.connection.cursor().fetchone.return_value = (1,)
        project = db_interface.get_project_by_name('test_project', 1)
        db_interface.db.connection.cursor().execute.assert_called_once()
        db_interface.db.connection.cursor().fetchone.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
        assert project == (1,)

    def test_get_user(self, db_interface):
        db_interface.db.connection.cursor().fetchone.return_value = (
            1, 'test_name', 'test_email', 'test_password')
        user = db_interface.get_user('test_email')
        db_interface.db.connection.cursor().execute.assert_called_once()
        db_interface.db.connection.cursor().fetchone.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
        assert user == (1, 'test_name', 'test_email', 'test_password')

    def test_get_user_by_mail(self, db_interface):
        db_interface.db.connection.cursor().fetchone.return_value = (
            1, 'test_name', 'test_email', 'test_password')
        user = db_interface.get_user_by_mail('test_email')
        db_interface.db.connection.cursor().execute.assert_called_once()
        db_interface.db.connection.cursor().fetchone.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
        assert user == (1, 'test_name', 'test_email', 'test_password')

    def test_get_stages(self, db_interface):
        time = '2023-5-2 20:06:20'
        db_interface.db.connection.cursor().fetchall.return_value = [
            (1, 'stage_name', 1, 0, 0, 0, time), (2, 'stage_name2', 1, 0, 0, 0, time)]
        stages = db_interface.get_stages(project_id=1, user_id=1)
        db_interface.db.connection.cursor().execute.assert_called_once()
        db_interface.db.connection.cursor().fetchall.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
        assert stages == [
            (1, 'stage_name', 1, 0, 0, 0, time), (2, 'stage_name2', 1, 0, 0, 0, time)]

    def test_get_stage(self, db_interface):
        time = '2023-5-2 20:06:20'
        db_interface.db.connection.cursor().fetchone.return_value = (
            1, 'stage_name', 1, 0, 0, 0, time)
        stage = db_interface.get_stage(1, 1, 1)
        db_interface.db.connection.cursor().execute.assert_called_once()
        db_interface.db.connection.cursor().fetchone.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
        assert stage == (
            1, 'stage_name', 1, 0, 0, 0, time)

    '''UPDATE TESTS'''

    def test_update_user_name(self, db_interface):
        db_interface.update_user_name(1, 'new_name')
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE users SET name = %s WHERE id = %s''',
            ('new_name', 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_user_email(self, db_interface):
        db_interface.update_user_email(1, 'new_email')
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE users SET email = %s WHERE id = %s''',
            ('new_email', 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_user_password(self, db_interface):
        db_interface.update_user_password(1, 'new_password')
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE users SET password = %s WHERE id = %s''',
            ('new_password', 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_project_name(self, db_interface):
        db_interface.update_project_name(1, 'new_project_name')
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE projects SET name = %s WHERE id = %s''',
            ('new_project_name', 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_stage_name(self, db_interface):
        db_interface.update_stage_name(1, 'new_stage_name')
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE stages SET stage_name = %s WHERE id = %s''',
            ('new_stage_name', 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_stage_days(self, db_interface):
        db_interface.update_stage_days(1, 2)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE stages SET days = %s WHERE id = %s''',
            (2, 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_stage_seconds(self, db_interface):
        db_interface.update_stage_seconds(1, 2)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE stages SET seconds = %s WHERE id = %s''',
            (2, 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_stage_price(self, db_interface):
        db_interface.update_stage_price(1, 2)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE stages SET price = %s WHERE id = %s''',
            (2, 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_update_stage_last_updated(self, db_interface):
        db_interface.update_stage_last_updated(1, time)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''UPDATE stages SET last_updated = %s WHERE id = %s''',
            (time, 1))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    '''DELETE TESTS'''

    def test_delete_user(self, db_interface):
        db_interface.delete_user(1)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''DELETE FROM users WHERE id = %s''',
            (1,))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_delete_project(self, db_interface):
        db_interface.delete_project(1)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''DELETE FROM projects WHERE id = %s''',
            (1,))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()

    def test_delete_stage(self, db_interface):
        db_interface.delete_stage(1)
        db_interface.db.connection.cursor().execute.assert_called_once_with(
            '''DELETE FROM stages WHERE id = %s''',
            (1,))
        db_interface.db.connection.commit.assert_called_once()
        db_interface.db.connection.cursor().close.assert_called_once()
