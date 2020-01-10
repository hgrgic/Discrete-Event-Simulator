from main.core.model.exceptions.internal.SetupException import SetupException


class DatabaseConfigurationException(SetupException):
    def __init__(self, message):
        super().__init__(message)