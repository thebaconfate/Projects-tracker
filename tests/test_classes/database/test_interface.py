import pytest
from unittest.mock import patch, AsyncMock
from src.classes.database.interface import DatabaseInterface


class TestDatabaseInterface:

    @pytest.fixture
    def mysql_patch(self):
        yield patch("mysql.connector.aio.connect", new_callable=AsyncMock)

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

    @pytest.mark.asyncio
    async def test_aenter_called(
        self, database_interface_patch, database_args, mysql_patch
    ):
        with mysql_patch:
            with patch(
                database_interface_patch + ".__aenter__", new_callable=AsyncMock
            ) as mock_aenter:
                async with DatabaseInterface(**database_args):
                    pass
                assert mock_aenter.called

    @pytest.mark.asyncio
    async def test_aexit_called(
        self, database_interface_patch, mysql_patch, database_args
    ):
        with mysql_patch:
            with patch(
                database_interface_patch + ".__aexit__", new_callable=AsyncMock
            ) as mock_aexit:
                async with DatabaseInterface(**database_args):
                    pass
                assert mock_aexit.called

    @pytest.mark.asyncio
    async def test_database_interface(self, mysql_patch, database_args):
        """Test that the database interface can be created and connected to a database,\
            this tests the following methods: __init__, __connect, __aenter__, __close, __aexit__"""
        with mysql_patch as mock_connect:
            mock_connection = mock_connect.return_value
            async with DatabaseInterface(**database_args) as db_interface:
                # Test that connection is established
                assert mock_connect.called
            # Test that connection is closed after exiting the with block
            mock_connection.close.assert_called_once()
