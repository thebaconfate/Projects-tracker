class DatabaseError(Exception):
    """Base class for database errors"""
    def __init__(self, message = "An error occurred with the database"):
        self.message = message
        super().__init__(self.message)


class DatabaseConnectionError(DatabaseError):
    """Error raised when a connection to the database cannot be established"""
    def __init__(self, message = "Could not establish connection to database"):
        self.message = message
        super().__init__(self.message)


class DatabaseCursorError(DatabaseError):
    """Error raised when a cursor cannot be established to the database"""
    def __init__(self, message = "Could not establish cursor to database"):
        self.message = message
        super().__init__(self.message)


class DatabaseUserError(DatabaseError):
    """Error raised when an error occurs with the user"""
    def __init__(self, message = "An error occurred with the user"):
        self.message = message
        super().__init__(self.message)


class DatabaseUserAlreadyExistsError(DatabaseUserError):
    """Error raised when a user already exists in the database"""
    def __init__(self, message="User already exists"):
        self.message = message
        super().__init__(self.message)
