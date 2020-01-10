from main.core.model.exceptions.internal.SecurityException import SecurityException


class DatabaseAccessException(SecurityException):
    def __init__(self, message):
        super().__init__(message)