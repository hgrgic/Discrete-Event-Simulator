from main.core.model.simulation.State import State


class Cpu:
    def __init__(self, cpu_name, units):
        self.cpu_name = cpu_name
        self.entity_type = "CPU"

        self.max_cpu_units = units
        self.available_cpu_units = units

    def reserve_resources(self, units):
        # TODO: define business logic
        return -1

    def release_resources(self, units):
        # TODO: define business logic
        return -1

    def get_state(self, parent_entity) -> State:
        return State(self.cpu_name, self.entity_type, self.max_cpu_units, self.available_cpu_units, parent_entity)