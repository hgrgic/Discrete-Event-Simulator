from main.core.model.exceptions.BadRequestExceptions import BadRequestException


class ConfigurationSetupMismatch(BadRequestException):
    def __init__(self, message):
        super().__init__(message)