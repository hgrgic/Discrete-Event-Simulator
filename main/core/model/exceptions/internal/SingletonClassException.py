from main.core.model.exceptions.InternalExceptions import InternalException


class SingletonClassException(InternalException):
    def __init__(self, message):
        super().__init__(message)