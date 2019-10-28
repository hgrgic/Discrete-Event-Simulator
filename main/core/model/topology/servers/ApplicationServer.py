from main.core.model.simulation.State import State
from main.core.model.topology.components.Cpu import Cpu
from main.core.model.topology.components.Disk import Disk


class ApplicationServer:

    def __init__(self, server_name):
        self.server_name = server_name
        self.entity_type = "APP_SERVER"

        self.cumulative_cpu_units = 0
        self.cumulative_disk_units = 0
        self.available_disk_units = 0
        self.available_cpu_units = 0
        self.attached_disks = dict()
        self.attached_cpus = dict()

    def attach_cpus(self, cpus):
        for cpu in cpus:
            _cpu = Cpu(cpu['name'], cpu['units'])
            self.attach_cpu(_cpu)

    def attach_disks(self, disks):
        for disk in disks:
            _disk = Disk(disk['name'], disk['units'])
            self.attach_disk(_disk)

    def attach_cpu(self, cpu: Cpu):
        self.cumulative_cpu_units += cpu.max_cpu_units
        self.available_cpu_units += cpu.available_cpu_units
        self.attached_cpus[cpu.cpu_name] = cpu

    def attach_disk(self, disk: Disk):
        self.cumulative_disk_units += disk.max_disk_units
        self.available_disk_units += disk.available_disk_units
        self.attached_disks[disk.disk_name] = disk

    def record_trnsaction(self, number_of_transactions):
        # TODO: define business logic
        return -1

    def get_available_resources(self):
        # TODO: define business logic
        return -1

    def get_state(self, parent_entity=None) -> State:
        dependent_states = []
        for cpu in self.attached_cpus.values():
            dependent_states.append(cpu.get_state(self.server_name))

        for disk in self.attached_disks.values():
            dependent_states.append(disk.get_state(self.server_name))

        return State(self.server_name, self.entity_type, None, None, dependent_states=dependent_states)