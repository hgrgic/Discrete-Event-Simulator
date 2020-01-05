from main.core.model.simulation.State import State
from main.core.model.topology.components.Disk import Disk


class DatabaseServer:

    def __init__(self, server_name, sim_env):
        self.server_name = server_name
        self.entity_type = "DB_SERVER"
        self.sim_env = sim_env

        self.cumulative_disk_units = 0
        self.available_disk_units = 0
        self.attached_disks = dict()

    def attach_disks(self, disks):
        for disk in disks:
            _disk = Disk(disk['name'], disk['units'], self.sim_env)
            self.attach_disk(_disk)

    def attach_disk(self, disk: Disk):
        self.cumulative_disk_units += disk.max_disk_units
        self.available_disk_units += disk.available_disk_units.count
        self.attached_disks[disk.disk_name] = disk

    def store_transaction(self, transaction):
        # TODO: define business logic
        return -1

    def get_available_resources(self):
        # TODO: define business logic
        return -1

    def get_state(self, parent_entity=None) -> State:
        dependent_states = []
        for disk in self.attached_disks.values():
            dependent_states.append(disk.get_state(self.server_name))

        return State(self.server_name, self.entity_type,
                     self.cumulative_disk_units, self.available_disk_units, dependent_states=dependent_states)
