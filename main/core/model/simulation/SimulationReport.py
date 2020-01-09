import jsonpickle
import json
from bson.json_util import dumps


class SimulationReport:
    def __init__(self) -> None:
        self.report = []

    def compile_report(self, topology):
        for key in topology.keys():
            for component in topology[key]:
                self.report.append({"name": component.server_name, "type": component.entity_type, "metrics": component.get_states()})

    @staticmethod
    def get_reports(collection):
        document = collection.find({}, {"_id":0, "report":0})
        return dumps(document)

    @staticmethod
    def get_report(runtime_id, collection):
        document = collection.find_one({"runtime_id": runtime_id}, {"_id":0})
        return document

    def save_report(self, runtime_id, simulation_name, simulation_description,
                    simulation_start_time, simulation_finish_time,  collection):
        document = dict(runtime_id=runtime_id, simulation_name=simulation_name,
                        simulation_description=simulation_description, start_time=str(simulation_start_time),
                        finish_time=str(simulation_finish_time), report=self.report)

        result = collection.insert_one(document)
        return result.inserted_id

    @staticmethod
    def delete_report(runtime_id, collection):
        db_response = collection.delete_one({'runtime_id': runtime_id})
        return db_response.deleted_count
