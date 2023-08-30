
from datetime import datetime
import sys
from unittest.mock import MagicMock, Mock, patch
import unittest
import os

from classes.database import databaseinterface

sys.path.append(os.path.abspath('..../src'))
sys.path.append(os.path.abspath('....'))
#! keep from src.classes.database.databaseinterface import databaseinterface below the sys.path.append


class DatabaseInterfaceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.database = Mock()
        cls.database_interface = databaseinterface(cls.database)
        cls.user_name_values = {'accepted': ['string', None],
                                'rejected': [1, 1.5, True, False, [], {}, ()]}
        cls.email_values = {'accepted': ['string'],
                            'rejected': [1, 1.5, True, None, False, [], {}, ()]}
        cls.password_values = {'accepted': ['string'],
                               'rejected': [1, 1.5, True, None, False, [], {}, ()]}
        cls.project_name_values = {'accepted': ['string'],
                                   'rejected': [1, 1.5, True, None, False, [], {}, ()]}
        cls.project_owner_values = {'accepted': [1],
                                    'rejected': ['string', 1.5, True, None, False, [], {}, ()]}
        cls.stage_name_values = {'accepted': ['string'],
                                 'rejected': [1, 1.5, True, None, False, [], {}, ()]}
        cls.stage_project_id_values = {'accepted': [1],
                                       'rejected': ['string', 1.5, True, None, False, [], {}, ()]}
        cls.stage_days_values = {'accepted': [1],
                                 'rejected': ['string', 1.5, True, None, False, [], {}, ()]}
        cls.stage_seconds_values = {'accepted': [1],
                                    'rejected': ['string', 1.5, True, None, False, [], {}, ()]}
        cls.stage_price_values = {'accepted': [1, 1.5],
                                  'rejected': ['string', True, None, False, [], {}, ()]}
        cls.stage_last_updated_values = {'accepted': [datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')],
                                         'rejected': ['string', True, None, False, [], {}, (), 1, 1.5]}

    def setUp(self):
        self.database.connection.cursor().execute = MagicMock()
        self.database.connection.commit = MagicMock()
        self.database.connection.cursor().close = MagicMock()

    def test_insert_user(self):
        self.database_interface.insert_user(
            self.user_name_values['accepted'][0], self.email_values['accepted'][0], self.password_values['accepted'][0])
        self.database.connection.cursor().execute.assert_called_once_with(
            '''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (self.user_name_values['accepted'][0], self.email_values['accepted'][0], self.password_values['accepted'][0]))
        self.database.connection.commit.assert_called_once()
        self.database.connection.cursor().close.assert_called_once()

    def test_insert_user_null_name(self):
        self.database_interface.insert_user(
            self.user_name_values['accepted'][1], self.email_values['accepted'][0], self.password_values['accepted'][0])
        self.database.connection.cursor().execute.assert_called_once_with(
            '''INSERT INTO users (name, email, password) VALUES (%s, %s, %s)''', (self.user_name_values['accepted'][1], self.email_values['accepted'][0], self.password_values['accepted'][0]))
        self.database.connection.commit.assert_called_once()
        self.database.connection.cursor().close.assert_called_once()

    def test_insert_user_with_invalid_name(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.user_name_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_user(
                    value, self.email_values['accepted'][0], self.password_values['accepted'][0])

    def test_insert_user_with_invalid_email(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.email_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_user(
                    self.user_name_values['accepted'][0], value, self.password_values['accepted'][0])

    def test_insert_user_with_invalid_password(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.password_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_user(
                    self.user_name_values['accepted'][0], self.email_values['accepted'][0], value)

    def insert_project(self):
        self.database_interface.insert_project(
            self.project_name_values['accepted'][0], self.project_owner_values['accepted'][0])
        self.database.connection.cursor().execute.assert_called_once_with(
            '''INSERT INTO projects (name, owner) VALUES (%s, %s)''', (self.project_name_values['accepted'][0], self.project_owner_values['accepted'][0]))
        self.database.connection.commit.assert_called_once()
        self.database.connection.cursor().close.assert_called_once()

    def test_insert_project_with_invalid_name(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.project_name_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_project(
                    value, self.project_owner_values['accepted'][0])

    def test_insert_project_with_invalid_owner(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.project_owner_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_project(
                    self.project_name_values['accepted'][0], value)

    def test_insert_stage(self):
        self.database_interface.insert_stage(
            self.stage_name_values['accepted'][0], self.stage_project_id_values['accepted'][0], self.stage_days_values['accepted'][0], self.stage_seconds_values['accepted'][0], self.stage_price_values['accepted'][0], self.stage_last_updated_values['accepted'][0])
        self.database.connection.cursor().execute.assert_called_once_with(
            '''INSERT INTO stages (stage_name, project_id, days, seconds, price, last_updated) VALUES (%s, %s, %s, %s, %s, %s)''', (self.stage_name_values['accepted'][0], self.stage_project_id_values['accepted'][0], self.stage_days_values['accepted'][0], self.stage_seconds_values['accepted'][0], self.stage_price_values['accepted'][0], self.stage_last_updated_values['accepted'][0]))
        self.database.connection.commit.assert_called_once()
        self.database.connection.cursor().close.assert_called_once()

    def test_insert_stage_with_invalid_name(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.stage_name_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_stage(
                    value, self.stage_project_id_values['accepted'][0], self.stage_days_values['accepted'][0], self.stage_seconds_values['accepted'][0], self.stage_price_values['accepted'][0], self.stage_last_updated_values['accepted'][0])

    def test_insert_stage_with_invalid_project_id(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.stage_project_id_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_stage(
                    self.stage_name_values['accepted'][0], value, self.stage_days_values['accepted'][0], self.stage_seconds_values['accepted'][0], self.stage_price_values['accepted'][0], self.stage_last_updated_values['accepted'][0])

    def test_insert_stage_with_invalid_days(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.stage_days_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_stage(
                    self.stage_name_values['accepted'][0], self.stage_project_id_values['accepted'][0], value, self.stage_seconds_values['accepted'][0], self.stage_price_values['accepted'][0], self.stage_last_updated_values['accepted'][0])

    def test_insert_stage_with_invalid_seconds(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.stage_seconds_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_stage(
                    self.stage_name_values['accepted'][0], self.stage_project_id_values['accepted'][0], self.stage_days_values['accepted'][0], value, self.stage_price_values['accepted'][0], self.stage_last_updated_values['accepted'][0])

    def test_insert_stage_with_invalid_price(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.stage_price_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_stage(
                    self.stage_name_values['accepted'][0], self.stage_project_id_values['accepted'][0], self.stage_days_values['accepted'][0], self.stage_seconds_values['accepted'][0], value, self.stage_last_updated_values['accepted'][0])

    def test_insert_stage_with_invalid_last_updated(self):
        self.database.connection.cursor().execute = TypeError('error')
        for value in self.stage_last_updated_values['rejected']:
            with self.assertRaises(TypeError):
                self.database_interface.insert_stage(
                    self.stage_name_values['accepted'][0], self.stage_project_id_values['accepted'][0], self.stage_days_values['accepted'][0], self.stage_seconds_values['accepted'][0], self.stage_price_values['accepted'][0], value)


if __name__ == '__main__':
    unittest.main()
