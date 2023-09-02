from unittest import mock
from unittest.mock import Mock

import pytest

"""Some constants for testing"""
time = "2020-01-01 00:00:00"
id = 1
name = "test_name"
email = "test_email@email.com"
password = "test_password"
project_id = 1
project_name = "test_project"
stage_id = 1
stage_name = "test_stage"
days = 1
seconds = 1
price = 1.5
owner_id = 1
test_projects = [(1, "test_project"), (2, "test_project2")]
disconnect = "src.classes.database.databaseinterface.DatabaseInterface.disconnect"
connect = "src.classes.database.databaseinterface.DatabaseInterface.connect"


class TestDataBaseInterface:
    #! ALWAYS KEEP MOCK_CONNECT AS SECOND PARAMETER IN TESTS!
    #! ALWAYS KEEP MOCK_DISCONNECT AS THIRD PARAMETER IN TESTS!
    """The mocks are passed through positionally."""

    """INSERT TESTS"""

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_connect(self, mock_connect, mock_disconnect, db_interface):
        mysql, cursor = db_interface.connect()
        mock_connect.assert_called_once()
        assert mysql == mock_connect.return_value[0]
        assert cursor == mock_connect.return_value[1]

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_disconnect(self, mock_connect, mock_disconnect, db_interface):
        mysql = db_interface.connect()[0]
        db_interface.disconnect(mysql)
        mock_disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_insert_user(self, mock_connect, mock_disconnect, db_interface):
        db_interface.insert_user(name, email, password)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """INSERT INTO users (name, email, password) VALUES (%s, %s, %s)""",
            (name, email, password),
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_insert_project(self, mock_connect, mock_disconnect, db_interface):
        mysql, cursor = mock_connect.return_value
        db_interface.insert_project(project_name, owner_id)
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """INSERT INTO projects (name, owner_id) VALUES (%s, %s)""",
            (project_name, owner_id),
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_insert_stage(self, mock_connect, mock_disconnect, db_interface):
        mysql, cursor = mock_connect.return_value
        db_interface.insert_stage(stage_name, project_id, days, seconds, price, time)
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """INSERT INTO stages (stage_name, project_id, days, seconds, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)""",
            (stage_name, project_id, days, seconds, price, time),
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    """SELECT TESTS"""

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_get_projects(self, mock_connect, mock_disconnect, db_interface):
        projects = db_interface.get_projects(1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """SELECT id, name FROM projects where owner_id = %s;""", (1,)
        )
        cursor.fetchall.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_get_project(self, mock_connect, mock_disconnect, db_interface):
        project = db_interface.get_project(1, 1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """SELECT id, name FROM projects where owner_id = %s AND id = %s;""", (1, 1)
        )
        cursor.fetchone.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_get_project_by_name(self, mock_connect, mock_disconnect, db_interface):
        project = db_interface.get_project_by_name(project_name, 1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """SELECT id FROM projects where owner_id = %s AND name = %s;""",
            (1, project_name),
        )
        cursor.fetchone.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_get_user(self, mock_connect, mock_disconnect, db_interface):
        user = db_interface.get_user(1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """SELECT id, name, email, password FROM users WHERE id = %s""", (1,)
        )
        cursor.fetchone.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_get_user_by_mail(self, mock_connect, mock_disconnect, db_interface):
        user = db_interface.get_user_by_mail("test_email")
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """SELECT id, name, email, password FROM users WHERE email = %s""",
            ("test_email",),
        )
        cursor.fetchone.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_get_stages(self, mock_connect, mock_disconnect, db_interface):
        stages = db_interface.get_stages(1, 1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """SELECT stages.id, stage_name, project_id, last_updated FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE projects.id = %s AND users.id = %s ORDER BY stages.id ASC;""",
            (1, 1),
        )
        cursor.fetchall.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_get_stage(self, mock_connect, mock_disconnect, db_interface):
        stage = db_interface.get_stage(1, 1, 1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """SELECT stages.id, stage_name, project_id, days, seconds, price, last_updated  FROM ((stages LEFT JOIN projects ON projects.id = stages.project_id) LEFT JOIN users ON projects.owner_id = users.id) WHERE stages.id = %s AND projects.id = %s and users.id = %s ;""",
            (1, 1, 1),
        )
        cursor.fetchone.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    """UPDATE TESTS"""

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_user_name(self, mock_connect, mock_disconnect, db_interface):
        mysql, cursor = mock_connect.return_value
        db_interface.update_user_name(1, "new_name")
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE users SET name = %s WHERE id = %s""", ("new_name", 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_user_email(self, mock_connect, mock_disconnect, db_interface):
        db_interface.update_user_email(1, "new_email")
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE users SET email = %s WHERE id = %s""", ("new_email", 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_user_password(self, mock_connect, mock_disconnect, db_interface):
        db_interface.update_user_password(1, "new_password")
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE users SET password = %s WHERE id = %s""", ("new_password", 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_project_name(self, mock_connect, mock_disconnect, db_interface):
        db_interface.update_project_name(1, "new_project_name")
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE projects SET name = %s WHERE id = %s""", ("new_project_name", 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_stage_name(self, mock_connect, mock_disconnect, db_interface):
        db_interface.update_stage_name(1, "new_stage_name")
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE stages SET stage_name = %s WHERE id = %s""", ("new_stage_name", 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_stage_days(self, mock_connect, mock_disconnect, db_interface):
        db_interface.update_stage_days(1, 2)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE stages SET days = %s WHERE id = %s""", (2, 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_stage_seconds(self, mock_connect, mock_disconnect, db_interface):
        db_interface.update_stage_seconds(1, 2)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE stages SET seconds = %s WHERE id = %s""", (2, 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_stage_price(self, mock_connect, mock_disconnect, db_interface):
        db_interface.update_stage_price(1, 2.5)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE stages SET price = %s WHERE id = %s""", (2.5, 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_update_stage_last_updated(
        self, mock_connect, mock_disconnect, db_interface
    ):
        db_interface.update_stage_last_updated(1, "new_time")
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """UPDATE stages SET last_updated = %s WHERE id = %s""", ("new_time", 1)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    """DELETE TESTS"""

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_delete_user(self, mock_connect, mock_disconnect, db_interface):
        db_interface.delete_user(1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """DELETE FROM users WHERE id = %s""", (1,)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_delete_project(self, mock_connect, mock_disconnect, db_interface):
        db_interface.delete_project(1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """DELETE FROM projects WHERE id = %s""", (1,)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)

    @mock.patch(disconnect)
    @mock.patch(connect, return_value=(Mock(), Mock()))
    def test_delete_stage(self, mock_connect, mock_disconnect, db_interface):
        db_interface.delete_stage(1)
        mysql, cursor = mock_connect.return_value
        db_interface.connect.assert_called_once()
        cursor.execute.assert_called_once_with(
            """DELETE FROM stages WHERE id = %s""", (1,)
        )
        mysql.commit.assert_called_once()
        db_interface.disconnect.assert_called_once_with(mysql)
