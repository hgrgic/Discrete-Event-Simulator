from __future__ import annotations

import datetime

from main.core.model.exceptions.internal.SingletonClassException import SingletonClassException
from main.core.model.exceptions.request.NoSuchElementException import NoSuchElementException
from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.infrastructure.ConfigurationConstants import REPORT_COLLECTION
from main.core.service.infrastructure.MongoAdapter import MongoAdapter
from main.core.service.operations.Simulator import Simulator


class OperationsController:
    __instance = None

    def __init__(self):
        if OperationsController.__instance is not None:
            raise SingletonClassException("Instance already exists!")
        else:
            OperationsController.__instance = self
            self.__instance.__running_simulations = {}

    @staticmethod
    def get_instance() -> OperationsController:
        if OperationsController.__instance is None:
            OperationsController()
        return OperationsController.__instance

    def register_simulation(self, simulation: Simulator, runtime_id):
        if self.__instance is not None:
            start_time = datetime.datetime.now()
            self.__instance.__running_simulations[runtime_id] = {
                'start_time': datetime.datetime.now(),
                "name": simulation.name,
                "description": simulation.description,
                "simulation": simulation,
            }
            print(f"Simulation {runtime_id} started at {start_time}")
            simulation.start_simulation(runtime_id)
            return runtime_id
        else:
            raise SingletonClassException("Singleton not instantiated")

    def complete_simulation_runtime(self, runtime_id, report: SimulationReport):
        if self.__instance is not None:
            if runtime_id in self.__instance.__running_simulations:
                instance = self.__instance.__running_simulations[runtime_id]
                finish_time = datetime.datetime.now()

                mongo = MongoAdapter()
                mongo.open_db_connection()
                reports_collection = mongo.get_collection(REPORT_COLLECTION)

                report.save_report(runtime_id, instance['name'], instance['description'], instance['start_time'],
                                   finish_time, reports_collection)

                print(f"Simulation {runtime_id} finished at {finish_time}")
                del self.__instance.__running_simulations[runtime_id]
            else:
                raise NoSuchElementException("Element with runtime_id '%s' not found!" % runtime_id)
        else:
            raise SingletonClassException("Singleton not instantiated")

    def get_all_running_simulations(self):
        if self.__instance is not None:
            in_process = []
            for key in self.__instance.__running_simulations.keys():
                in_process.append({
                    "runtime_id": key,
                    "name":self.__instance.__running_simulations[key]['name'],
                    "description":self.__instance.__running_simulations[key]['description'],
                    "start_time":self.__instance.__running_simulations[key]['start_time'],
                })
            return in_process
        else:
            raise SingletonClassException("Singleton not instantiated")

    def get_running_simulation(self, runtime_id):
        if self.__instance is not None:
            if runtime_id in self.__instance.__running_simulations:
                return self.__instance.__running_simulations[runtime_id]
            else:
                raise NoSuchElementException("Element with runtime_id '%s' not found!" % runtime_id)
        else:
            raise SingletonClassException("Singleton not instantiated")