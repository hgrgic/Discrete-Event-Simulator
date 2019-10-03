
class Cpu:
    def __init__(self, cpu_name, units):
        self.cpu_name = cpu_name
        self.max_cpu_units = units
        self.available_cpu_units = units

    def reserve_resources(self, units):
        # TODO: define business logic
        return -1

    def release_resources(self, units):
        # TODO: define business logic
        return -1