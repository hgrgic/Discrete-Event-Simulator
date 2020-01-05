import simpy

from main.core.model.simulation import Event
from main.core.model.simulation.State import State


class ApplicationServer:

    def __init__(self, server_name, sim_env, cpu_units, memory_units):
        self.server_name = server_name
        self.entity_type = "APP_SERVER"
        self.sim_env = sim_env

        self.cpu_units = simpy.Resource(sim_env, capacity=cpu_units)
        self.memory_units = simpy.Resource(sim_env, capacity=memory_units)

    def execute_event(self, event: Event):
        with self.cpu_units.request() as cpu_req:  # EVENT NOT USED, MEMORY NOT USED!!!
            yield cpu_req
            yield self.sim_env.timeout(1)
            self.debug_cpu_stats()

    def get_resources(self):
        """
        Tuple returning as the first value the count of currently processing units, as second value the len of the queue
        """
        processing = {'cpu': self.cpu_units.count, 'memory': self.memory_units.count}
        queue = {'cpu': len(self.cpu_units.queue), 'memory': len(self.memory_units.queue)}
        return processing, queue

    def debug_cpu_stats(self):
        print('%s - %d of %d CPU slots are allocated.' % (self.server_name, self.cpu_units.count, self.cpu_units.capacity))
        print('\tTime:', self.sim_env.now)
        print('\tUsers:', len(self.cpu_units.users))
        print('\tQueued events:', len(self.cpu_units.queue))

    def debug_memory_stats(self):
        print('%s - %d of %d MEMORY slots are allocated.' % (self.server_name, self.memory_units.count, self.memory_units.capacity))
        print('\tTime:', self.sim_env.now)
        print('\tUsers:', len(self.memory_units.users))
        print('\tQueued events:', len(self.memory_units.queue))

    def get_state(self) -> State:
        return None
    #     return State(self.server_name, self.entity_type, None, None, dependent_states=dependent_states)
