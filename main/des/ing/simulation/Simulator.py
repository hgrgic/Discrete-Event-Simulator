from main.core.service.topology.ToplogyManager import TopologyManager


class Simulator(object):
    def __init__(self, _env, _scenario, _topology_manager: TopologyManager):
        self.env = _env
        self.duration = _scenario['simulation_duration_days']
        self.workload = _scenario['workload']
        self.topology_manager = _topology_manager
        self.runtime_id = None

        # Start the run process every time an instance is created.
        self.action = _env.process(self._run())

    def start_simulation(self, runtime_id):
        self.runtime_id = runtime_id
        self.env.run(until=self.duration)

    def _run(self):
        while True:
            for event in self.workload:
                print(f'Time: {self.env.now}')
                yield self.env.process(self.topology_manager.process_event(self.env, event))
