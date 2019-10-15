import random

from main.core.model.exceptions.internal.SetupException import SetupException
from main.core.model.exceptions.request.ConfigurationSetupMismatch import ConfigurationSetupMismatch
from main.core.model.exceptions.request.NoSuchElementException import NoSuchElementException
from main.core.model.exceptions.request.ProportionOverloadException import ProportionOverloadException
from main.core.service.operations.Event import Event
from main.core.util.StatUtility import get_gamma_dist, get_norm_dist, get_binomial_dist


class ScenarioBuilder:

    def __init__(self) -> None:
        super().__init__()
        self.simulation_budget = 0
        self.simulation_duration = 0
        self.events = []
        self.simulation_dist = None

    def instantiate_scenario(self, scenario):
        try:
            self.simulation_duration = scenario["duration_days"]
            self.simulation_budget = scenario['simulation_budget']

            if scenario["gamma_distribution"] is not None:
                self.simulation_dist = get_gamma_dist(self.simulation_budget, scenario["gamma_distribution"]['a'])

            if scenario["normal_distribution"] is not None:
                self.simulation_dist = get_norm_dist(self.simulation_budget, scenario["normal_distribution"]['center'])

            if sum(scenario["event_proportions"]) > 1.0:
                raise ProportionOverloadException("Sum of proportions greater than 1")
            if len(scenario["event_proportions"]) != len(scenario["event_prototypes"]):
                raise ConfigurationSetupMismatch("Length mismatch between defined proportions and prototypes")

            for i in range(len(scenario["event_proportions"])):
                self._build_events_list(scenario["event_prototypes"][i], scenario["event_proportions"][i])

            return self._export_sim_scenario()

        except KeyError as ke:
            raise NoSuchElementException("Key %s is missing or has not been properly defined." % ke)


    def _build_events_list(self, prototype, proportion):
        local_budget = round(self.simulation_budget * proportion)
        error_bin_dist = get_binomial_dist(local_budget, prototype['error_proportion'])

        for i in range(local_budget):
            raise_incident = True if error_bin_dist[i] else False
            event = Event(prototype['type'], prototype['weight'], raise_incident)
            self.events.append(event)

    def _export_sim_scenario(self):
        random.shuffle(self.events)
        if len(self.events) != len(self.simulation_dist):
            raise SetupException("Length mismatch between defined events and assigned distribution")

        for i in range(len(self.events)):
            self.events[i].set_size(self.simulation_dist[i])

        return {"simulation_duration_days": self.simulation_duration, "simulation_events": self.events}
