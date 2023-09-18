from datetime import timedelta
from marshmallow import Schema, fields, post_load
from src.classes.models.stage import Stage

#! doesn't serialize timedelta as it's not a field in the schema.


class StageSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    project_id = fields.Int(required=True)
    time = fields.TimeDelta(load_default=timedelta(days=0, seconds=0))
    last_updated = fields.DateTime()

    @post_load
    def make_stage(self, data, **kwargs):
        return Stage(**data)
