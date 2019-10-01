from main.core.model.topology.components.Disk import Disk


class DatabaseServer:

    def __init__(self, server_name):
        self.server_name = server_name

        self.cumulative_disk_units = 0
        self.available_disk_units = 0
        self.attached_disks = dict()

    def attach_disks(self, disks):
        for disk in disks:
            _disk = Disk(disk['name'], disk['units'])
            self.attach_disk(_disk)

    def attach_disk(self, disk: Disk):
        self.cumulative_disk_units += disk.max_disk_units
        self.available_disk_units += disk.available_disk_units
        self.attached_disks[disk.disk_name] = disk

    def store_transaction(self, transaction):
        return -1

    def get_available_resources(self):
        return -1

