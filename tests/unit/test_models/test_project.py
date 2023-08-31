
class TestProject():

    def test_new_project_with_fixture(self, new_project):
        assert new_project.id == 1
        assert new_project.name == 'test_name'
        assert new_project.owner_id == 1
        