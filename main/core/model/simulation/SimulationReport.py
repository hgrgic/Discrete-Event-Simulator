from main.core.model.simulation.SystemSnapshot import SystemSnapshot


class SimulationReport:
    def __init__(self) -> None:
        super().__init__()
        self.snapshots = []

    def append_snapshot(self, system_snapshot):
        if type(system_snapshot) is list:
            self.snapshots += system_snapshot
        else:
            self.snapshots.append(system_snapshot.associated_states)