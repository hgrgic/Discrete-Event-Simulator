import simpy

from main.core.model.simulation import Event

CPU_COMPONENT = 'cpu'
MEMORY_COMPONENT = 'memory'


class ApplicationServer:

    def __init__(self, server_name, sim_env, cpu_units, memory_units):
        self.server_name = server_name
        self.entity_type = "APP_SERVER"
        self.sim_env = sim_env

        self.cpu_units = simpy.resources.container.Container(sim_env, capacity=cpu_units, init=0)
        self.memory_units = simpy.resources.container.Container(sim_env, capacity=memory_units, init=0)

        self.states = {CPU_COMPONENT: [], MEMORY_COMPONENT: []}

    def execute_event(self, event: Event, step):
        yield self.sim_env.timeout(step)
        self.cpu_units.put(event.weight)
        yield self.sim_env.timeout(0)
        self.record_state(CPU_COMPONENT, self.sim_env.now, self.cpu_units)  # recording CPU activity
        self.record_state(MEMORY_COMPONENT, self.sim_env.now, self.memory_units)  # recording RAM activity
        self.cpu_units.get(event.weight)

    # TODO: refactor once multi CPU feature under development
    def get_resources(self):
        """
        Tuple returning as the first value the count of currently processing units, as second value the len of the queue
        """
        processing = {'cpu': 10, 'memory': 10}
        queue = {'cpu': 10, 'memory': 10}
        return processing, queue

    def record_state(self, component, env_time, container):
        self.states[component].append([env_time, round(container.level, 3), len(container.put_queue)])
