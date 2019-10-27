from flask import make_response, jsonify, request, abort
from flask_restful import Resource

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.service.operations.OperationsController import OperationsController


class SimulationController(Resource):

    def get(self):
        try:
            oc = OperationsController.get_instance()
            if request.args.get("id") is not None:
                runtime_id = request.args.get("id")
                return make_response(jsonify(oc.get_running_simulation(runtime_id)), 200)
            else:
                return make_response(jsonify({"in_process": oc.get_all_running_simulations()}), 200)
        except BadRequestException as bre:
            abort(400, {"error": bre.args})