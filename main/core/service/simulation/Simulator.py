from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.operations.ToplogyManager import TopologyController
import pandas as pd
import matplotlib.pyplot as plt


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
            self.topology_controller.process_event(self.env, step_events, step)

        self.env.run()

        debug_states(self.topology_controller.topology.get('application-servers')[0].states['cpu'])  # TODO: remove for production

        simulation_report = SimulationReport()
        simulation_report.compile_report(self.topology_controller.topology)
        oc.complete_simulation_runtime(self.runtime_id, simulation_report)


def debug_states(data):
    data_frame = pd.DataFrame(data,
                              columns=["step", "cpu_usage", "cpu_queue"])
    data_frame = data_frame.groupby(["step"]).max()
    # data_frame.to_csv('rep.csv')

    plt.subplot(2, 1, 1)
    plt.plot(data_frame["cpu_usage"])
    plt.title("CPU_usage")
    plt.margins()
    plt.subplot(2, 1, 2)
    plt.plot(data_frame["cpu_queue"])
    plt.title("Requests in queue")
    plt.subplots_adjust(hspace=0.5)
    plt.show()