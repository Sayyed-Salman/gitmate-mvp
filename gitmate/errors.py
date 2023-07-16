class CustomException(Exception):
    """Base class for exceptions"""
    pass


class FileExistsError(CustomException):
    """Raised when file already exists"""

    def __init__(self, *args: object, message) -> None:
        self.message = message
        super().__init__(*args, self.message)


class FileNotFoundError(CustomException):
    """Raised when file not found"""

    def __init__(self, *args: object, message) -> None:
        self.message = message
        super().__init__(*args, self.message)
