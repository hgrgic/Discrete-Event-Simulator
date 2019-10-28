from main.core.model.simulation import Event


class TopologyManager:

    def __init__(self, topology) -> None:
        super().__init__()
        self.topology = topology

    def process_event(self, env, event: Event):
        # TODO: define business logic
        # TODO: pass event to correct topology elements
        yield env.timeout(1)