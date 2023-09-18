from datetime import datetime, timedelta
from pytz import UTC

# TODO convert days and seconds to timedelta to autoconvert seconds to days.
# TODO merge should add the timedelta's together.


class Stage:
    def __init__(
        self,
        project_id=None,
        name=None,
        id=None,
        price=0,
        time=timedelta(days=0,seconds=0),
        last_updated=None,
    ):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.price = price
        self.time = time 
        self.last_updated = last_updated

    def get_last_updated(self):
        utc = self.last_updated.astimezone(UTC)
        return utc.strftime("%Y-%m-%d %H:%M:%S")

    def merge(self, other_stage):
        self.time += other_stage.time
        self.last_updated = datetime.utcnow()

    def __repr__(self):
        return "<Stage(id={self.id!r}, project_id={self.project_id!r})>".format(
            self=self
        )
