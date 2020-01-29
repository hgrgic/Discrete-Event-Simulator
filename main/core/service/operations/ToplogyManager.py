from main.core.model.exceptions.InternalExceptions import InternalException


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

            optimal_cpu_container.put(event.weight)
            optimal_server.record_state(optimal_cpu_index, env.now, optimal_cpu_container, "IN", event.name)

            yield env.timeout(event.load_time)  # processing takes one time step

            optimal_cpu_container.get(event.weight)
            optimal_server.record_state(optimal_cpu_index, env.now, optimal_cpu_container, "OUT", event.name)
        else:
            raise InternalException("Simulation failed. Optimal server could not be determined!")

    def process_anomaly(self, env, incident):
        yield env.timeout(incident.start_step)  # this yields a NEW event at its corresponding start step

        server = self.topology.get('application-servers')[incident.target_server_index]
        cpu = server.get_cpu_container(incident.target_cpu_index)

        cpu.put(cpu.capacity)
        server.record_state(incident.target_cpu_index, env.now, cpu, "IN", incident.name)

        yield env.timeout(incident.duration)

        cpu.get(cpu.capacity)

        server.record_state(incident.target_cpu_index, env.now, cpu, "OUT", incident.name)
