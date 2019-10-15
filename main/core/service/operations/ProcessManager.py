from main.core.service.topology.ToplogyManager import TopologyManager


class ProcessManager:

    def __init__(self, _process_manager: TopologyManager) -> None:
        super().__init__()
        self._process_manager = _process_manager

    def process_event(self, event_type, event_number):
        return -1