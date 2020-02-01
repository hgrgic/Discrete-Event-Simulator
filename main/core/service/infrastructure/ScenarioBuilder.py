import random

import simpy

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.model.simulation.Event import Event
from main.core.model.simulation.Incident import Incident
from main.core.util.StatUtility import get_poisson_dist, generate_intervals_load_times_and_names


class ScenarioBuilder:

    def __init__(self) -> None:
        super().__init__()
        self.events = []
        self.incidents = []

    def instantiate_scenario(self, scenario):
        if len(scenario["events_per_hour"]) == len(scenario["distribution_per_hour"]) == len(scenario["load_times_per_hour"]):
            intervals_day, load_times_day, names_day = generate_intervals_load_times_and_names(scenario["events_per_hour"],
                                                                                           scenario["distribution_per_hour"],
                                                                                           scenario["load_times_per_hour"])

            for i in range(len(intervals_day)):
                self.events.append(Event(intervals_day[i], load_times_day[i], names_day[i]))

            for incident in scenario['incidents']:
                self.incidents.append(Incident(incident['name'],
                                               incident['target_server_index'],
                                               incident['target_cpu_index'],
                                               incident['start'], incident['duration']))

            return {"events": self.events, "incidents": self.incidents}
        else:
            raise BadRequestException("Lengths of scenario components must match")

    def get_sim_environment(self):
        env = simpy.Environment()
        return env