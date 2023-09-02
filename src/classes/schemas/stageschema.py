from marshmallow import Schema, fields, post_load
from src.classes.models.stage import Stage


class StageSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    project_id = fields.Int(required=True)
    days = fields.Int(load_default=0)
    seconds = fields.Int(load_default=0)
    price = fields.Float(load_default=0.0)
    last_updated = fields.DateTime()

    @post_load
    def make_stage(self, data, **kwargs):
        return Stage(**data)
