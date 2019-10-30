from flask import make_response, jsonify, request, abort
from flask_restful import Resource

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.service.operations.OperationsController import OperationsController


class SimulationController(Resource):

    def get(self):
        try:
            oc = OperationsController.get_instance()
            if request.args.get("runtime_id") is not None:  # get a single running simulation
                runtime_id = request.args.get("runtime_id")
                _simulation = oc.get_running_simulation(runtime_id)
                return make_response(jsonify({"runtime_id": runtime_id, "start_time": _simulation["start_time"]}), 200)
            else:
                return make_response(jsonify({"in_process": oc.get_all_running_simulations()}), 200)  # get all  running simulations
        except BadRequestException as bre:
            abort(400, {"error": bre.args})
