import pytest
from unittest.mock import patch, AsyncMock
from src.classes.database.interface import DatabaseInterface


class TestDatabaseInterface:

    @pytest.fixture(autouse=True)
    def mock_connect(self):
        with patch(
            "mysql.connector.aio.connect", new_callable=AsyncMock
        ) as mock_connect:
            yield mock_connect

    @pytest.fixture
    def database_args(self):
        yield {
            "host": "localhost",
            "database": "testdb",
            "user": "testuser",
            "password": "testpassword",
            "port": 3306,
        }

    @pytest.fixture
    def database_interface_patch(self):
        yield "src.classes.database.interface.DatabaseInterface"

    @pytest.fixture
    def test_user(self):
        yield {
            "id": 1,
            "username": "testuser",
            "email": "testemail",
            "password": "testpassword",
        }

    @pytest.mark.asyncio
    async def test_aenter_called(self, database_interface_patch, database_args):
        """Test that the __aenter__ method is called when entering the context manager"""
        with patch(
            database_interface_patch + ".__aenter__", new_callable=AsyncMock
        ) as mock_aenter:
            async with DatabaseInterface(**database_args):
                pass
            assert mock_aenter.called

    @pytest.mark.asyncio
    async def test_aenter_raises_exception(self, mock_connect, database_args):
        # Configure mock to raise an exception when called
        mock_connect.side_effect = Exception()
        with pytest.raises(Exception):
            async with DatabaseInterface(**database_args):
                # This code should raise an exception during connection attempt
                pass

    @pytest.mark.asyncio
    async def test_aexit_called(self, database_interface_patch, database_args):
        """Test that the __aexit__ method is called when exiting the context manager"""
        with patch(
            database_interface_patch + ".__aexit__", new_callable=AsyncMock
        ) as mock_aexit:
            async with DatabaseInterface(**database_args):
                pass
            assert mock_aexit.called

    @pytest.mark.asyncio
    async def test_database_interface(self, mock_connect, database_args):
        """Test that the database interface creates a connection when calling __aenter__ and closes a connection when calling __aexit__ within the context manager"""
        mock_connect = mock_connect
        mock_connection = mock_connect.return_value
        async with DatabaseInterface(**database_args):
            # Test that connection is established
            assert mock_connect.called
        # Test that connection is closed after exiting the with block
        mock_connection.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_user_by_email(
        self, mock_connect: AsyncMock, database_args, test_user
    ):
        """Test that the get_user method returns the user from the database"""
        # user to be fetched from the database
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = test_user
        expected_result = (
            mock_connect.return_value.cursor.return_value.fetchone.return_value
        )
        async with DatabaseInterface(**database_args) as db:
            result = await db.get_user_by_email(test_user["email"])
        mock_connect.return_value.cursor.assert_called_once()
        mock_cursor.execute.assert_called_with(
            "SELECT * FROM users WHERE email = %s", (test_user["email"],)
        )
        mock_cursor.fetchone.assert_called_once()
        assert result.model_dump() == expected_result

    @pytest.mark.asyncio
    async def test_get_user_by_email_no_user(
        self, mock_connect: AsyncMock, database_args, test_user
    ):
        """Test that the get_user method returns None if the user is not found in the database"""
        # user to be fetched from the database
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchone.return_value = None
        async with DatabaseInterface(**database_args) as db:
            result = await db.get_user_by_email(test_user["email"])
        mock_connect.return_value.cursor.assert_called_once()
        mock_cursor.execute.assert_called_with(
            "SELECT * FROM users WHERE email = %s", (test_user["email"],)
        )
        mock_cursor.fetchone.assert_called_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_save_user(self, mock_connect, database_args, test_user):
        """Test that the save_user method inserts a new user into the database"""
        # Values to be saved to the database, excluding the id
        del test_user["id"]
        values = tuple(test_user.values())
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchone.return_value = None
        async with DatabaseInterface(**database_args) as db:
            await db.save_user(*values)
        """The method should first test if the user already exists."""
        mock_connection.cursor.assert_called_once()
        assert (
            mock_connection.cursor.return_value.execute.call_count == 2
        )  # should have queried the database and saved the user = 2 execution calls
        mock_connection.cursor.return_value.fetchone.assert_called_once()
        """If the user does not exist, the method should insert the user into the database."""
        # Test that the query is executed
        mock_connection.cursor.return_value.execute.assert_called_with(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            values,
        )
        # Test that the connection is committed
        mock_connection.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_save_user_existing_user(
        self, mock_connect, database_args, test_user
    ):
        """Test that the save_user method raises an exception if the user already exists"""
        # Values to be saved to the database, excluding the id
        del test_user["id"]
        values = tuple(test_user.values())
        mock_connection = mock_connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchone.return_value = test_user
        async with DatabaseInterface(**database_args) as db:
            with pytest.raises(Exception):
                await db.save_user(*values)
        mock_connection.cursor.assert_called_once()
        mock_connection.cursor.return_value.execute.assert_called_once()
        mock_connection.commit.assert_not_called()

