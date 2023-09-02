from ...conftest import test_pass, test_user_email, test_user_name


class TestUser:
    def test_new_user_with_fixture(self, new_user):
        assert new_user.id == 1
        assert new_user.name == test_user_name
        assert new_user.email == test_user_email
        assert new_user.password == test_pass

    def test_user_password_hashing_with_fixture(self, new_user):
        password = new_user.password
        new_user.hash_password()
        assert new_user.password != password
        assert new_user.check_password(password) is True
