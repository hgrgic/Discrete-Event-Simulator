from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.model.topology.servers.ApplicationServer import CPU_COMPONENT, MEMORY_COMPONENT


class TopologyController:

    def __init__(self, topology) -> None:
        super().__init__()
        self.topology = topology

    def process_event(self, env, event):
        yield env.timeout(event.interval_time)  # this yields a NEW event at its corresponding start step

        optimal_server = None
        optimal_cpu_index = None
        optimal_cpu_container = None

        for server in self.topology.get('application-servers'):
            temp_optimal_server = server
            temp_cpu_index = server.get_optimal_cpu_index()
            temp_cpu_container = temp_optimal_server.get_cpu_container(temp_cpu_index)

            if optimal_server is None:
                optimal_server = temp_optimal_server
                optimal_cpu_index = temp_cpu_index
                optimal_cpu_container = temp_cpu_container
            else:
                if temp_cpu_container.capacity - temp_cpu_container.level - len(temp_cpu_container.put_queue) > optimal_cpu_container.capacity - optimal_cpu_container.level - len(optimal_cpu_container.put_queue):
                    optimal_server = temp_optimal_server
                    optimal_cpu_index = temp_cpu_index
                    optimal_cpu_container = temp_cpu_container

        if optimal_server is not None and optimal_cpu_index is not None and optimal_cpu_container is not None:

            optimal_server.record_state(optimal_cpu_index, env.now, optimal_cpu_container)
            optimal_cpu_container.put(event.weight)

            yield env.timeout(event.load_time)  # processing takes one time step
            optimal_server.record_state(optimal_cpu_index, env.now, optimal_cpu_container)

            optimal_cpu_container.get(event.weight)
        else:
            raise InternalException("Simulation failed. Optimal server could not be determined!")
