from marshmallow import Schema, fields, post_load
from classes.models.stage import Stage
from datetime import datetime
from pytz import timezone, utc


class StageSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    project_id = fields.Int(required=True)
    price = fields.Float(default=0.0)
    days = fields.Int(load_default=0)
    seconds = fields.Int(load_default=0)
    last_updated = fields.DateTime()

    @post_load
    def make_stage(self, data, **kwargs):
        return Stage(**data)
