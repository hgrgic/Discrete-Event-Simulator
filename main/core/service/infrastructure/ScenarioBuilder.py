import random

import simpy

from main.core.model.simulation.Event import Event
from main.core.util.StatUtility import get_poisson_dist


class ScenarioBuilder:

    def __init__(self) -> None:
        super().__init__()
        self.simulation_duration = 0
        self.events = {}
        self.simulation_dist = None

    def instantiate_scenario(self, scenario):
        self.simulation_duration = scenario['duration_days']
        self._build_step_events(self.simulation_duration, scenario["login_percentage"], scenario["step_avg"])
        return self._export_sim_scenario()

    def get_sim_environment(self):
        env = simpy.Environment()
        return env

    def _build_step_events(self, simulation_duration, login_percentage, step_avg):
        num_bins = 24 * simulation_duration
        step_dist = get_poisson_dist(num_bins, step_avg)

        for time_step in range(len(step_dist)):
            time_step_events = []
            for j in range(step_dist[time_step]):
                event = self.get_event_prototype(login_percentage)
                time_step_events.append(event)
            self.events[time_step] = time_step_events

    def get_event_prototype(self, login_percentage):
        if random.uniform(0, 1) > login_percentage:
            return Event("login", 0.001, False)  # login event prototype
        else:
            return Event("transaction", 0.005, False)  # transaction event prototype

    def _export_sim_scenario(self):
        return {"simulation_duration_days": self.simulation_duration, "workload": self.events}
