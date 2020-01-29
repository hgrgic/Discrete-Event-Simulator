from flask import request, abort, make_response, jsonify
from flask_restful import Resource
from flask_restful_swagger import swagger

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.service.operations.OperationsController import OperationsController


class SimulationsWebController(Resource):

    @swagger.operation(
        notes='Get all running simulations.',
        responseMessages=[
            {
                "code": 200,
                "message": "List of summaries for running simulation."
            },
            {
                "code": 400,
                "message": "Error, Bad Request"
            }
        ]
    )
    def get(self):
        try:
            oc = OperationsController.get_instance()
            return make_response(jsonify({"in_process": oc.get_all_running_simulations()}), 200)
        except BadRequestException as bre:
            abort(400, {"error": bre.args})
