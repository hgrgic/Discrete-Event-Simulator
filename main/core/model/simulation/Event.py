
class Event:

    def __init__(self, _type, _weight, _raise_incident, _size) -> None:
        super().__init__()
        self.type = _type
        self.weight = _weight
        self.size = _size
        self.raise_incident = _raise_incident
