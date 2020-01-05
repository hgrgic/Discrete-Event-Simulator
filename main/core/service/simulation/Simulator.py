from main.core.service.operations.ToplogyManager import TopologyController


class Simulator(object):
    def __init__(self, _env, _scenario, _topology_controller: TopologyController):
        self.env = _env
        self.duration = _scenario['simulation_duration_days']
        self.workload = _scenario['workload']
        self.topology_controller = _topology_controller
        self.runtime_id = None

    def start_simulation(self, runtime_id):
        self.runtime_id = runtime_id

        from main.core.service.operations.OperationsController import OperationsController
        oc = OperationsController.get_instance()

        for step in self.workload:
            step_events = self.workload[step]
            self.topology_controller.process_event(self.env, step_events, step)
            # oc.get_running_simulation(self.runtime_id)['report'].append_snapshot(snap) # TODO: implement as part of reporting

        self.env.run()

        oc.complete_simulation_runtime(self.runtime_id)