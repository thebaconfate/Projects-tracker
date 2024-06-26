class AuthenticationError(Exception):
    """Base class for authentication errors"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(AuthenticationError):
    """Error raised when the user is not found in the database"""

    def __init__(self, message: str = "User not found"):
        super().__init__(message)


class SecretKeyError(AuthenticationError):
    """Error raised when SECRET_KEY is not set"""

    def __init__(self, message: str = "SECRET_KEY not set"):
        super().__init__(message)


class HashingAlgorithmError(AuthenticationError):
    """Error raised when HASHING_ALGORITHM is not set"""

    def __init__(self, message: str = "HASHING_ALGORITHM not set"):
        super().__init__(message)


class IncorrectPasswordError(AuthenticationError):
    """Error raised when the password provided does not match the hashed password in the database"""

    def __init__(self, message: str = "Incorrect password"):
        super().__init__(message)


class InvalidTokenException(AuthenticationError):
    """Error raised when the token is invalid"""

    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)
