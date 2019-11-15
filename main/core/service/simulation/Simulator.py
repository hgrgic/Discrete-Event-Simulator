from main.core.service.operations.ToplogyManager import TopologyController


class Simulator(object):
    def __init__(self, _env, _scenario, _topology_controller: TopologyController):
        self.env = _env
        self.duration = _scenario['simulation_duration_days']
        self.workload = _scenario['workload']
        self.topology_controller = _topology_controller
        self.runtime_id = None

        # Start the run process every time an instance is created.
        self.action = _env.process(self._run())

    def start_simulation(self, runtime_id):
        self.runtime_id = runtime_id
        self.env.run(until=self.duration)

    def _run(self):
        from main.core.service.operations.OperationsController import OperationsController
        oc = OperationsController.get_instance()
        while True:
            for event in self.workload:
                print(f'Time: {self.env.now}')
                snap = yield self.env.process(self.topology_controller.process_event(self.env, event))
                oc.get_running_simulation(self.runtime_id)['report'].append_snapshot(snap)

                # TODO: close simulation after completed