from main.core.model.incidents.critical import CriticalIncident


class DiskFailureIncident(CriticalIncident):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)