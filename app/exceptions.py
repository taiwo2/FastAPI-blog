class CredentialsException(Exception):
    """
    Exception raised when authentication credentials are invalid.
    """
    def __init__(self, message: str = "Could not validate credentials"):
        self.message = message
        super().__init__(self.message)

class NotFoundException(Exception):
    """
    Exception raised when a requested resource is not found.
    """
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)