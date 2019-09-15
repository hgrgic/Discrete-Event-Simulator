from main.core.model.incidents.critical import CriticalIncidentException


class DiskFullException(CriticalIncidentException):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)