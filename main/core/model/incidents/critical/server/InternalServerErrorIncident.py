from main.core.model.incidents.critical import CriticalIncident


class InternalServerErrorIncident(CriticalIncident):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)