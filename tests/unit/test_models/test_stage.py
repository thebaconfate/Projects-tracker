
from datetime import datetime


class TestStage():

    def test_new_stage_with_fixture(self,new_stage):
        assert new_stage.id == 1
        assert new_stage.name == 'test_name'
        assert new_stage.project_id == 1
        assert new_stage.price == 1.0
        assert new_stage.days == 1
        assert new_stage.seconds == 1
        assert new_stage.last_updated == datetime(2020, 1, 1, 0, 0, 0, 0)
    
    