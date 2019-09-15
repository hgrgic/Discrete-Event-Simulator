
class Cpu:
    def __init__(self, cpu_name, max_cpu_units):
        self.cpu_name = cpu_name
        self.max_cpu_units = max_cpu_units
        self.available_cpu_units = max_cpu_units
