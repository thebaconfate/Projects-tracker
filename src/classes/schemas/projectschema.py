from marshmallow import Schema, fields, post_load
from ..models.project import Project


class ProjectSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    owner_id = fields.Int(required=True)

    @post_load
    def make_project(self, data, **kwargs):
        return Project(**data)
