import math


class Event:

    def __init__(self, _type, _weight, _raise_incident, _next=None) -> None:
        super().__init__()
        self.type = _type
        self.weight = _weight
        self.size = 0
        self.raise_incident = _raise_incident
        self.next = _next

    def set_size(self, _size):
        self.size = math.ceil(math.fabs(_size))