from main.core.service.operations import Event


class TopologyManager:

    def __init__(self, topology) -> None:
        super().__init__()
        self.topology = topology

    def process_event(self, env, event:Event):
        # TODO: define business logic
        # TODO: pass event to correct topology elements
        yield env.timeout(1)

    def add_topology_component(self, toplogy_element):
        # TODO: define business logic
        return -1

    def stop_topology_component(self, toplogy_element):
        # TODO: define business logic
        return -1

    def remove_topology_component(self, toplogy_element):
        # TODO: define business logic
        return -1