
class TopologyController:

    def __init__(self, topology) -> None:
        super().__init__()
        self.topology = topology

    def process_event(self, env, events):
        for event in events:
            optimal_server = None
            for idx in range(len(self.topology.get('application-servers'))):  # find optimal app server (does not work)
                server = self.topology.get('application-servers')[idx]
                if idx == 0:
                    optimal_server = server
                else:
                    if server.get_resources()[1].get('cpu') < optimal_server.get_resources()[1].get('cpu'):
                        optimal_server = server

                env.process(optimal_server.execute_event(event))

        # snapshot = SystemSnapshot(self._get_system_snapshot(self.topology))  # after event execution, take snapshot #TODO: implement as part of reporting
        # return snapshot

    def _get_system_snapshot(self, entities):
        states = []
        for entity in entities:
            if type(entity) is str:
                states += self._get_system_snapshot(entities[entity])
            else:
                states.append(entity.get_state())
        return states
