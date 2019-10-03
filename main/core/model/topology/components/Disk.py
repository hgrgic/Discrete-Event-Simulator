

class Disk:
    def __init__(self, disk_name, units):
        self.disk_name = disk_name
        self.max_disk_units = units
        self.available_disk_units = units

    def store_event(self, units):
        # TODO: define business logic
        return -1
