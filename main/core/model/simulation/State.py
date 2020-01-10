from __future__ import annotations


class State:
    def __init__(self, name, entity_type, total_units, available_units, parent_entity=None, dependent_states=None) -> None:
        self.name = name
        self.entity_type = entity_type
        self.total_units = total_units
        self.available_units = available_units
        self.parent_entity = parent_entity
        self.dependent_states = dependent_states

    def add_dependent_state(self, state: State):
        if self.dependent_states is None:
            self.dependent_states = []
        self.dependent_states.append(state)
