from main.core.model.exceptions.InternalExceptions import InternalException


class SetupException(InternalException):
    def __init__(self, message):
        super().__init__(message)