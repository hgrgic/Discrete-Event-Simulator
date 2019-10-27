from __future__ import annotations

import datetime

from main.core.model.exceptions.internal.SingletonClassException import SingletonClassException
from main.core.model.exceptions.request.NoSuchElementException import NoSuchElementException
from main.core.util.IdentityUtility import get_unique_id
from main.des.ing.simulation.Simulator import Simulator


class OperationsController:
    __instance = None

    def __init__(self):
        if OperationsController.__instance is not None:
            raise SingletonClassException("This class is a singleton!")
        else:
            OperationsController.__instance = self
            self.__instance.__running_simulations = {}

    @staticmethod
    def get_instance() -> OperationsController:
        if OperationsController.__instance is None:
            OperationsController()
        return OperationsController.__instance

    def register_simulation(self, simulation: Simulator):
        if self.__instance is not None:
            runtime_id = get_unique_id()
            self.__instance.__running_simulations[runtime_id] = {'start_time': datetime.datetime.now(), "simulation": simulation}
            simulation.start_simulation(runtime_id)
            return runtime_id
        else:
            raise SingletonClassException("Singleton not instantiated")

    def complete_simulation_runtime(self, runtime_id):
        if self.__instance is not None:
            # TODO: optionally store to database finish time, results
            del self.__instance.__running_simulations[runtime_id]
        else:
            raise SingletonClassException("Singleton not instantiated")

    def get_all_running_simulations(self):
        if self.__instance is not None:
            return list(self.__instance.__running_simulations.keys())
        else:
            raise SingletonClassException("Singleton not instantiated")

    def get_running_simulation(self, runtime_id):
        if self.__instance is not None:
            if runtime_id in self.__instance.__running_simulations:
                _simulation = self.__instance.__running_simulations[runtime_id]
                return {"runtime_id": runtime_id, "start_time": _simulation["start_time"]}
            else:
                raise NoSuchElementException("Element with runtime_id '%s' not found!" % runtime_id)
        else:
            raise SingletonClassException("Singleton not instantiated")
