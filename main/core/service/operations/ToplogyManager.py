from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.model.topology.servers.ApplicationServer import CPU_COMPONENT, MEMORY_COMPONENT


class TopologyController:

    def __init__(self, topology) -> None:
        super().__init__()
        self.topology = topology

    def process_event(self, env, event):
        optimal_server = self.topology.get('application-servers')[0]
        # for event in events:
        #     optimal_server = None
        #     for idx in range(len(self.topology.get('application-servers'))):  # find optimal app server (does not work)
        #         server = self.topology.get('application-servers')[idx]
        #         if idx == 0:
        #             optimal_server = server
        #         else:
        #             if server.get_resources().get('cpu') < optimal_server.get_resources().get('cpu'):
        #                 optimal_server = server

        if optimal_server is not None:
            yield env.timeout(event.interval_time) # this yields a NEW event at its corresponding start step

            cpu_index = optimal_server.get_optimal_cpu_index()
            cpu_container = optimal_server.get_cpu_container(cpu_index)

            print("Server:", optimal_server.server_name, "CPU:", str(cpu_index))
            optimal_server.record_state(cpu_index, env.now, cpu_container)
            cpu_container.put(event.weight)
            # Print_recourse_metrics(cpu_container, "M_post_put") =========

            # process by cpu unit
            yield env.timeout(event.load_time) # processing takes one time step
            # print(f'STEP {env.now} POST - {name}')
            optimal_server.record_state(cpu_index, env.now, cpu_container)

            cpu_container.get(event.weight)
            # Print_recourse_metrics(cpu_container, "M_post_get") =========

        else:
            raise InternalException("Optimal server could not be determined!")
