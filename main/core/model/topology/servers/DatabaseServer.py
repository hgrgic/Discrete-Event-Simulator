import simpy

from main.core.model.simulation import Event

DISK_COMPONENT = 'disk'


class DatabaseServer:

    def __init__(self, server_name, sim_env, disk_units):
        self.server_name = server_name
        self.entity_type = "DB_SERVER"
        self.sim_env = sim_env
        self.disk_units = simpy.resources.container.Container(sim_env, capacity=disk_units, init=0)
        self.states = {DISK_COMPONENT: []}

    def execute_event(self, event: Event, step):
        yield self.sim_env.timeout(step)
        self.disk_units.put(event.weight)
        yield self.sim_env.timeout(0)
        self.record_state(DISK_COMPONENT, self.sim_env.now, self.cpu_units)
        self.cpu_units.get(event.weight)

    # TODO: refactor once multi CPU feature under development
    def get_resources(self):
        """
        Tuple returning as the first value the count of currently processing units as second value the len of the queue
        """
        processing = {'disk': 10}
        in_queue = {'disk': 10}
        return processing, in_queue

    def record_state(self, component, env_time, container):
        self.states[component].append([env_time, round(container.level, 3), len(container.put_queue)])
