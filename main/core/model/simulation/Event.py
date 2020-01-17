
class Event:

    def __init__(self, interval_time, load_time, name, weight=1):
        self.interval_time = interval_time
        self.load_time = load_time
        self.name = name
        self.weight = weight
