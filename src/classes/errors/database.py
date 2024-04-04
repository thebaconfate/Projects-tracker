class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseConnectionError(DatabaseError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseCursorError(DatabaseError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseUserError(DatabaseError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class DatabaseUserExistsError(DatabaseUserError):
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)
