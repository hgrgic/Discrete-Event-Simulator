import simpy

from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.model.simulation import Event
from main.core.model.topology.Reportable import Reportable

CPU_COMPONENT = 'cpu'
MEMORY_COMPONENT = 'memory'


class ApplicationServer(Reportable):

    def __init__(self, server_name, sim_env, cpu_sizes) -> None:
        super().__init__()
        self.server_name = server_name
        self.entity_type = "APP_SERVER"
        self.sim_env = sim_env

        self.cpu_list = []
        self._generate_cpu(cpu_sizes)



    def execute_event(self):
        return self.cpu_units, self.memory_units

    def get_cpu_container(self, index):
        return self.cpu_list[index]

    def _generate_cpu(self, cpu_sizes):
        for e, i in enumerate(cpu_sizes):
            self.cpu_list.append(simpy.resources.container.Container(self.sim_env, capacity=i, init=0))
            super().register_component("C"+str(e))

    def get_optimal_cpu_index(self):
        if len(self.cpu_list) > 0:
            optimal_idx = 0
            for e, i in enumerate(self.cpu_list):
                if i.capacity - i.level - len(i.put_queue) > self.cpu_list[optimal_idx].capacity - self.cpu_list[optimal_idx].level - len(self.cpu_list[optimal_idx].put_queue):
                    optimal_idx = e

            return optimal_idx
        else:
            raise InternalException("CPUs not allocated on the topology element!")
