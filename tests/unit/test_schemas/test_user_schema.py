import pytest
from src.classes.models.user import User
from src.classes.schemas.userschema import UserSchema


class TestUserSchemaWithFixture:
    @pytest.fixture(scope="class")
    def user_schema_values(self):
        return {
            "id": 1,
            "name": "test_name",
            "email": "test_email@email.com",
            "password": "test_password",
        }

    @pytest.fixture(scope="class")
    def wrong_user_id(self):
        return ["hello", "d", [], {}, (), None]

    @pytest.fixture(scope="class")
    def wrong_user_name(self):
        return [1, 1.0, True, False, [], {}, (), None]

    @pytest.fixture(scope="class")
    def wrong_user_email(self):
        return [1, 1.0, True, False, [], {}, (), "test_email", None]

    @pytest.fixture(scope="class")
    def wrong_user_password(self):
        return [1, 1.0, True, False, [], {}, (), None]

    def test_user_schema_load(self, user_schema_values):
        self.schema = UserSchema()
        user = self.schema.load(
            {
                "id": user_schema_values["id"],
                "name": user_schema_values["name"],
                "email": user_schema_values["email"],
                "password": user_schema_values["password"],
            }
        )
        assert user.id == user_schema_values["id"]
        assert user.name == user_schema_values["name"]
        assert user.email == user_schema_values["email"]
        assert user.password == user_schema_values["password"]

    def test_user_schema_load_no_pass_with_fixture(self, user_schema_values):
        self.schema = UserSchema()
        with pytest.raises(Exception):
            self.schema.load(
                {
                    "id": user_schema_values["id"],
                    "name": user_schema_values["name"],
                    "email": user_schema_values["email"],
                }
            )

    def test_user_schema_load_no_email_with_fixture(self, user_schema_values):
        with pytest.raises(Exception):
            self.schema.load(
                {
                    "id": user_schema_values["id"],
                    "name": user_schema_values["name"],
                    "password": user_schema_values["password"],
                }
            )

    def test_user_schema_load_no_name_with_fixture(self, user_schema_values):
        with pytest.raises(Exception):
            self.schema.load(
                {
                    "id": user_schema_values["id"],
                    "email": user_schema_values["email"],
                    "password": user_schema_values["password"],
                }
            )

    def test_user_schema_load_partial_id_with_fixture(self, user_schema_values):
        self.schema = UserSchema()
        user = self.schema.load(
            {
                "name": user_schema_values["name"],
                "email": user_schema_values["email"],
                "password": user_schema_values["password"],
            },
            partial=("id",),
        )
        assert user.name == user_schema_values["name"]
        assert user.email == user_schema_values["email"]
        assert user.password == user_schema_values["password"]

    def test_user_schema_load_wrong_id(self, user_schema_values, wrong_user_id):
        self.schema = UserSchema()
        for value in wrong_user_id:
            with pytest.raises(Exception):
                self.schema.load(
                    {
                        "id": value,
                        "name": user_schema_values["name"],
                        "email": user_schema_values["email"],
                        "password": user_schema_values["password"],
                    }
                )

    def test_user_schema_load_wrong_name(self, user_schema_values, wrong_user_name):
        self.schema = UserSchema()
        for value in wrong_user_name:
            with pytest.raises(Exception):
                self.schema.load(
                    {
                        "id": user_schema_values["id"],
                        "name": value,
                        "email": user_schema_values["email"],
                        "password": user_schema_values["password"],
                    }
                )

    def test_user_schema_load_wrong_email(self, user_schema_values, wrong_user_email):
        self.schema = UserSchema()
        for value in wrong_user_email:
            with pytest.raises(Exception):
                self.schema.load(
                    {
                        "id": user_schema_values["id"],
                        "name": user_schema_values["name"],
                        "email": value,
                        "password": user_schema_values["password"],
                    }
                )

    def test_user_schema_load_wrong_password(
        self, user_schema_values, wrong_user_password
    ):
        self.schema = UserSchema()
        for value in wrong_user_password:
            with pytest.raises(Exception):
                self.schema.load(
                    {
                        "id": user_schema_values["id"],
                        "name": user_schema_values["name"],
                        "email": user_schema_values["email"],
                        "password": value,
                    }
                )

    def test_user_partial_wrong(self, user_schema_values):
        self.schema = UserSchema()
        with pytest.raises(Exception):
            self.schema.load(
                {
                    "id": user_schema_values["id"],
                    "name": user_schema_values["name"],
                    "email": user_schema_values["email"],
                },
                partial=("password",),
            )

    def test_user_partial_correct(self, user_schema_values):
        self.schema = UserSchema()
        user = self.schema.load(
            {
                "password": user_schema_values["password"],
            },
            partial=("id", "name", "email"),
        )
        assert user.id == None
        assert user.name == None
        assert user.email == None
        assert user.password == user_schema_values["password"]

    def test_user_schema_dump(self, user_schema_values):
        self.schema = UserSchema()
        user = User(**user_schema_values)
        user_dict = self.schema.dump(user)
        assert user_dict["id"] == user_schema_values["id"]
        assert user_dict["name"] == user_schema_values["name"]
        assert user_dict["email"] == user_schema_values["email"]
        assert user_dict["password"] == user_schema_values["password"]

    def test_user_schema_dump_partial(self, user_schema_values):
        self.schema = UserSchema()
        user = User(**user_schema_values)
        user_dict = self.schema.dump(user)
        assert user_dict["id"] == user_schema_values["id"]
        assert user_dict["name"] == user_schema_values["name"]
        assert user_dict["email"] == user_schema_values["email"]
        assert user_dict["password"] == user_schema_values["password"]
