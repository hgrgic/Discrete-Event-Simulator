import jsonpickle
import json


class SimulationReport:
    def __init__(self) -> None:
        self.snapshots = []

    def append_snapshot(self, system_snapshot):
        if type(system_snapshot) is list:
            self.snapshots += system_snapshot
        else:
            self.snapshots.append(system_snapshot.associated_states)

    @staticmethod
    def get_report(runtime_id, collection):
        document = collection.find_one({"runtime_id": runtime_id})
        return document

    def save_report(self, runtime_id, collection):
        document = dict(runtime_id=runtime_id, snapshots=self.snapshots)
        document = json.loads(jsonpickle.encode(document, make_refs=False)) #encoding object to JSON
        result = collection.insert_one(document)
        return result.inserted_id

    @staticmethod
    def delete_report(runtime_id, collection):
        db_response = collection.delete_one({'runtime_id': runtime_id})
        return db_response.deleted_count
