from main.core.model.exceptions.BadRequestExceptions import BadRequestException


class ProportionOverloadException(BadRequestException):
    def __init__(self, message):
        super().__init__(message)