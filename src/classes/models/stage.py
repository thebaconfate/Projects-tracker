
class Stage():

    def __init__(self, id, name, project_id, price, days, seconds, last_update):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.price = price
        self.days = days
        self.seconds = seconds
        self.last_update = last_update

    def __repr__(self):
        return '<Stage(id={self.id!r}, project_id={self.project_id!r})>'.format(self=self)
