class Reportable:

    def __init__(self) -> None:
        self.states = {}

    def register_component(self, component):
        self.states[component] = []

    def record_state(self, component, env_time, container):
        self.states[component].append([env_time, round(container.level, 3), len(container.put_queue)])

    def get_states(self):
        return self.states
