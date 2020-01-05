import simpy

from main.core.model.simulation.State import State


class Disk:
    def __init__(self, disk_name, units, sim_env):
        self.disk_name = disk_name
        self.entity_type = "DISK"

        self.max_disk_units = units
        self.available_disk_units = simpy.Resource(sim_env, capacity=units)

    def store_event(self, units):
        # TODO: define business logic
        return -1

    def get_state(self, parent_entity) -> State:
        return State(self.disk_name, self.entity_type, self.max_disk_units, self.available_disk_units.count, parent_entity)
