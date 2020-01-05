import simpy

from main.core.model.simulation import Event
from main.core.model.simulation.State import State


class DatabaseServer:

    def __init__(self, server_name, sim_env, disk_units):
        self.server_name = server_name
        self.entity_type = "DB_SERVER"
        self.sim_env = sim_env
        self.disk_units = simpy.Resource(sim_env, capacity=disk_units)

    def execute(self, event: Event):
        with self.disk_units.request() as disk_req:  # EVENT NOT USED!!!
            yield disk_req
            yield self.sim_env.timeout(1)

    def get_resources(self):
        """
        Tuple returning as the first value the count of currently processing units
        as second value the len of the queue
        """
        processing = {'disk': self.disk_units.count}
        in_queue = {'disk': len(self.disk_units.queue)}
        return processing, in_queue

    def get_state(self, parent_entity=None) -> State:
        return None
        # dependent_states = []
        # for disk in self.attached_disks.values():
        #     dependent_states.append(disk.get_state(self.server_name))
        #
        # return State(self.server_name, self.entity_type,
        #              self.cumulative_disk_units, self.available_disk_units, dependent_states=dependent_states)
