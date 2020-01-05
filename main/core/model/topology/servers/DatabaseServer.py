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
            self.debug_disk_stats()

    def get_resources(self):
        """
        Tuple returning as the first value the count of currently processing units as second value the len of the queue
        """
        processing = {'disk': self.disk_units.count}
        in_queue = {'disk': len(self.disk_units.queue)}
        return processing, in_queue

    def debug_disk_stats(self):
        print('%s - %d of %d DISK slots are allocated.' % (self.server_name, self.disk_units.count, self.disk_units.capacity))
        print('\tTime:', self.sim_env.now)
        print('\tUsers:', len(self.disk_units.users))
        print('\tQueued events:', len(self.disk_units.queue))

    def get_state(self) -> State:
        return None