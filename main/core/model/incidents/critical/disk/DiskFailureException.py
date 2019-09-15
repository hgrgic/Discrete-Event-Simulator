from main.core.model.incidents.critical import CriticalIncidentException


class DiskFailureException(CriticalIncidentException):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)