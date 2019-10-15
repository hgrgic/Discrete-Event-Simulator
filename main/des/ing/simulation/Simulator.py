import simpy
from main.core.service.operations.ProcessManager import ProcessManager


class Simulator(object):
    def __init__(self, env, total_workload, process_manager: ProcessManager):
        self.env = env
        self.total_workload = total_workload
        self._process_manager = process_manager

        # Start the run process everytime an instance is created.
        self.action = env.process(self.run_simulator())

    def run_simulator(self):
        while True:
            print(f'Time: {self.env.now}')
            # workload_sample = random.choice(self.total_workload) #altering #TODO: replace with some values from JSON
            # print(f"Total workload: {workload_sample}") ### server part
            # We yield the process that process() returns
            # to wait for it to finish
            #yield self.env.process(self.server(workload_sample)) ### remove this part
            yield self._process_manager.process_event(-1,-1)