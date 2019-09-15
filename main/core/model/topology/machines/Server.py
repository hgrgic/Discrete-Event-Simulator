

class Server:

    def __init__(self, server_name):
        self.server_name = server_name

        self.cumulative_cpu_units = 0
        self.cumulative_disk_units = 0
        self.available_disk_units = 0
        self.available_cpu_units = 0
        self.attached_disks = []
        self.attached_cpus = []
