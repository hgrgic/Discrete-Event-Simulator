from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.model.topology.servers.ApplicationServer import CPU_COMPONENT, MEMORY_COMPONENT


class TopologyController:

    def __init__(self, topology) -> None:
        super().__init__()
        self.topology = topology

    def process_event(self, env, events, step):
        for event in events:
            optimal_server = None
            for idx in range(len(self.topology.get('application-servers'))):  # find optimal app server (does not work)
                server = self.topology.get('application-servers')[idx]
                if idx == 0:
                    optimal_server = server
                else:
                    if server.get_resources().get('cpu') < optimal_server.get_resources().get('cpu'):
                        optimal_server = server

            if optimal_server is not None:
                cpu, memory = optimal_server.execute_event(event, step)

                yield env.timeout(step)

                cpu.put(event.weight)
                memory.put(event.size)
                yield env.timeout(0)

                optimal_server.record_state(CPU_COMPONENT, env.now, cpu)  # recording CPU activity
                optimal_server.record_state(MEMORY_COMPONENT, env.now, memory)  # recording RAM activity

                cpu.get(event.weight)
                memory.get(event.size)

                print(optimal_server.server_name)

            else:
                raise InternalException("Optimal server could not be determined!")

    def _get_system_snapshot(self, entities):
        states = []
        for entity in entities:
            if type(entity) is str:
                states += self._get_system_snapshot(entities[entity])
            else:
                states.append(entity.get_state())
        return states
