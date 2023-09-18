from datetime import datetime, timedelta
from flask import logging
from src.classes.models.project import Project
from src.classes.schemas.projectschema import ProjectSchema
from src.classes.models.stage import Stage
from src.classes.database.databaseinterface import DatabaseInterface
from src.classes.customerrors.inputerror import InputException
from src.classes.schemas.stageschema import StageSchema


class Puthandler:
    """class to handle requests to update values"""

    def __init__(self):
        self.timeformat = "%Y-%m-%d %H:%M:%S"

    def switch_stage(self, db, stage, key, value, user):
        match key:
            case "name":
                guard_stage = db.get_stage_by_name(value, stage.project_id, user.id)
                if guard_stage is None:
                    db.update_stage_name(stage.id, value)
                else:
                    raise InputException("stage name already exists")
            case "price":
                db.update_stage_price(stage.id, value)
            case "time":
                last_updated = datetime.utcnow().strftime(self.timeformat)
                db.update_stage_days(stage.id, value.days)
                db.update_stage_seconds(stage.id, value.seconds)
                db.update_stage_last_updated(stage.id, last_updated)
            case _:
                """logging.error(
                    f"invalid payload key:{key} to update stage value: {value}"
                )"""
                raise InputException("invalid field to update stage")

    def update_stage(self, payload, user):
        schema = StageSchema()
        stage = schema.load(
            payload,
            partial=("name", "last_updated", "price", "time"),
        )
        with DatabaseInterface() as db:
            old_stage = db.get_stage(stage.project_id, stage.id, user.id)
            if old_stage is not None:
                old_stage["time"] = timedelta(
                    days=old_stage.pop("days"), seconds=old_stage.pop("seconds")
                )
                old_stage = Stage(**old_stage)
                for key in payload.keys():
                    if key != "id" or key != "project_id":
                        try:
                            self.switch_stage(
                                db, old_stage, key, stage.__getattribute__(key), user
                            )
                        except InputException:
                            continue
                stage = db.get_stage(stage.project_id, stage.id, user.id)
                stage["time"] = timedelta(
                    days=stage.pop("days"), seconds=stage.pop("seconds")
                )
                return schema.dump(Stage(**stage))
            else:
                raise InputException("""Couldn't find stage""")

    def add_time(self, payload, user):
        schema = StageSchema()
        stage = schema.load(
            payload,
            partial=(
                "id",
                "project_id",
                "last_updated",
                "price",
                "name",
            ),
        )
        with DatabaseInterface() as db:
            stored_stage = db.get_stage(stage.project_id, stage.id, user.id)
            if stored_stage is not None:
                stored_stage["time"] = timedelta(
                    days=stored_stage.pop("days"), seconds=stored_stage.pop("seconds")
                )
                stored_stage = Stage(**stored_stage)
                stored_stage.merge(stage)
                db.update_stage_days_seconds_last_updated(
                    stored_stage.id,
                    stored_stage.time.days,
                    stored_stage.time.seconds,
                    stored_stage.last_updated,
                )
        return schema.dump(stored_stage)

    def switch_project(self, db, key, value, project_id, user):
        match key:
            case "name":
                guard_project = db.get_project_by_name(value, project_id, user.id)
                if guard_project is None:
                    db.update_project_name(project_id, value)
                else:
                    raise InputException("project name already exists")
            case _:
                raise InputException("invalid payload to update project")

    def update_project(self, project_id, payload, user):
        schema = ProjectSchema()
        with DatabaseInterface() as db:
            project = db.get_project(project_id, user)
            if project is not None:
                schema = ProjectSchema()
                project = schema.load(project)
                for key in payload.keys():
                    if key != "id" or key != "project_id":
                        try:
                            self.switch_project(db, key, payload[key], project_id, user)
                        except InputException:
                            continue
                project = db.get_project(project_id, user)
                return schema.dump(Project(**project))
            else:
                raise InputException("Invalid project id")
