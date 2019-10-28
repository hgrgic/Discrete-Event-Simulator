from main.core.model.exceptions.BadRequestExceptions import BadRequestException


class NoSuchElementException(BadRequestException):
    def __init__(self, message):
            super().__init__(message)