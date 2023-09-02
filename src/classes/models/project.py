class Project:
    def __init__(self, id=None, name=None, owner_id=None):
        self.id = id
        self.name = name
        self.owner_id = owner_id

    def __repr__(self):
        return "<Project(id={self.id!r}, owner_id={self.owner_id!r})>".format(self=self)
