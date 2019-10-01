
class Cpu:
    def __init__(self, cpu_name, units):
        self.cpu_name = cpu_name
        self.max_cpu_units = units
        self.available_cpu_units = units
