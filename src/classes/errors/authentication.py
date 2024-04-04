class AuthenticationError(Exception):
    """Base class for authentication errors"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class SecretKeyError(AuthenticationError):
    """Error raised when SECRET_KEY is not set"""
    def __init__(self, message: str = "SECRET_KEY not set"):
        super().__init__(message)


class HashingAlgorithmError(AuthenticationError):
    """Error raised when HASHING_ALGORITHM is not set"""
    def __init__(self, message: str = "HASHING_ALGORITHM not set"):
        super().__init__(message)
