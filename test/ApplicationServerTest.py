import unittest

from main.core.model.topology.components.Cpu import Cpu
from main.core.model.topology.components.Disk import Disk
from main.core.model.topology.servers.ApplicationServer import ApplicationServer


class ApplicationServerAtomicOperations(unittest.TestCase):
    def test_attach_disk(self):
        server1 = ApplicationServer("AppServer1")
        disk1 = Disk("AppServer1_Disk1", 500)
        server1.attach_disk(disk1)
        self.assertEqual(server1.cumulative_disk_units, disk1.max_disk_units)

    def test_attach_cpu(self):
        server1 = ApplicationServer("AppServer1")
        cpu1 = Cpu("AppServer1_Cpu1", 1000)
        server1.attach_cpu(cpu1)
        self.assertEqual(server1.cumulative_cpu_units, cpu1.max_cpu_units)


if __name__ == '__main__':
    unittest.main()
