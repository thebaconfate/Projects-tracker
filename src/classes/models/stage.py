from datetime import datetime
from pytz import UTC


class Stage:
    def __init__(
        self,
        project_id=None,
        name=None,
        id=None,
        price=0,
        days=0,
        seconds=0,
        last_updated=None,
    ):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.price = price
        self.days = days
        self.seconds = seconds
        self.last_updated = last_updated

    def get_last_updated(self):
        utc = self.last_updated.astimezone(UTC)
        return utc.strftime("%Y-%m-%d %H:%M:%S")

    def merge(self, other_user):
        self.days += other_user.days
        self.seconds += other_user.seconds
        self.last_updated = datetime.utcnow()

    def __repr__(self):
        return "<Stage(id={self.id!r}, project_id={self.project_id!r})>".format(
            self=self
        )
