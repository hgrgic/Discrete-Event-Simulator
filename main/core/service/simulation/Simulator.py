from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.operations.ToplogyManager import TopologyController


class Simulator(object):
    def __init__(self, _env, _scenario, _topology_controller: TopologyController, name, description):
        self.env = _env
        self.duration = _scenario['simulation_duration_days']
        self.workload = _scenario['workload']
        self.topology_controller = _topology_controller
        self.runtime_id = None
        self.name = name
        self.description = description

    def start_simulation(self, runtime_id):
        self.runtime_id = runtime_id

        from main.core.service.operations.OperationsController import OperationsController
        oc = OperationsController.get_instance()

        for step in self.workload:
            step_events = self.workload[step]
            self.env.process(self.topology_controller.process_event(self.env, step_events, step))
            # self.topology_controller.process_event(self.env, step_events, step)

        self.env.run()

        simulation_report = SimulationReport()
        simulation_report.compile_report(self.topology_controller.topology)
        oc.complete_simulation_runtime(self.runtime_id, simulation_report)