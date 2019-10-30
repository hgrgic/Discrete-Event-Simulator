from main.core.model.simulation import Event
from main.core.model.simulation.SystemSnapshot import SystemSnapshot


class TopologyController:

    def __init__(self, topology) -> None:
        super().__init__()
        self.topology = topology

    def process_event(self, env, event: Event):
        # TODO: define business logic
        # TODO: pass event to correct topology elements
        snapshot = SystemSnapshot(self._get_system_snapshot(self.topology))  # after event execution, take snapshot
        yield env.timeout(1)
        return snapshot

    def process_events(self, env, events: []):
        snaps = []
        for event in events:
            # TODO: execute event
            snaps.append(SystemSnapshot(self._get_system_snapshot(self.topology)))  # after event execution, take snapshot
        yield env.timeout(1)
        return snaps

    def _get_system_snapshot(self, entities):
        states = []
        for entity in entities:
            if type(entity) is str:
                states += self._get_system_snapshot(entities[entity])
            else:
                states.append(entity.get_state())
        return states
