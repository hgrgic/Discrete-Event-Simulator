from __future__ import annotations


class Incident:
    def __init__(self, name, target_server_index, target_cpu_index, start_step, duration) -> None:
        self.name = name
        self.target_server_index = target_server_index
        self.target_cpu_index = target_cpu_index
        self.start_step = start_step
        self.duration = duration

