from threading import Thread

from flask_restful import Resource
from flask import request, abort, make_response, jsonify
from flask_restful_swagger import swagger

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.model.exceptions.request.NoSuchElementException import NoSuchElementException
from main.core.service.infrastructure.ScenarioBuilder import ScenarioBuilder
from main.core.service.operations.OperationsController import OperationsController
from main.core.service.operations.ToplogyManager import TopologyController
from main.core.service.infrastructure.TopologyBuilder import TopologyBuilder
from main.core.service.simulation.Simulator import Simulator
from main.core.util.IdentityUtility import get_unique_id


class SimulationWebController(Resource):

    @swagger.operation(
        notes='gets info about running simulation',
        parameters=[
            {
                "name": "runtime_id",
                "description": "Runtime ID of the respective simulation.",
                "required": True,
                "dataType": "String",
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Summary for respective running simulation."
            },
            {
                "code": 404,
                "message": "Error, No such element found."
            },
            {
                "code": 400,
                "message": "Error, Bad Request."
            }
        ]
    )
    def get(self):
        try:
            oc = OperationsController.get_instance()
            if request.args.get("runtime_id") is not None:
                runtime_id = request.args.get("runtime_id")
                _simulation = oc.get_running_simulation(runtime_id)
                return make_response(jsonify({
                    "runtime_id": runtime_id,
                    "start_time": _simulation["start_time"],
                    "name": _simulation["name"],
                    "description": _simulation["description"]
                }), 200)
            else:
                abort(400, {"error": "Bad request, missing query param runtime_id."})
        except NoSuchElementException as bre:
            abort(404, {"error": bre.args})
        except BadRequestException as bre:
            abort(400, {"error": bre.args})

    @swagger.operation(
        notes='Creates new simulation.',
        parameters=[
            {
                "name": "body",
                "description": "Blueprint for new simulation.",
                "required": True,
                "allowMultiple": False,
                "dataType": "Object",
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Summary for respective running simulation."
            },
            {
                "code": 404,
                "message": "Error, No such element found."
            },
            {
                "code": 400,
                "message": "Error, Bad Request."
            },
            {
                "code": 500,
                "message": "Error, Internal Error."
            }
        ]
    )
    def post(self):
        try:
            # Parsing simulation scenario
            sb = ScenarioBuilder()
            scenario = sb.instantiate_scenario(request.json['scenario'])
            sim_env = sb.get_sim_environment()

            # Parsing topology elements
            topology = TopologyBuilder.instantiate_topology(request.json['topology'], sim_env)
            topology_controller = TopologyController(topology)

            # Create simulation
            simulator = Simulator(sim_env, scenario, topology_controller, request.json['name'], request.json['description'])

            # Register and start simulation
            oc = OperationsController.get_instance()
            runtime_id = get_unique_id()
            thread = Thread(target=oc.register_simulation, args=(simulator, runtime_id,))
            thread.start()

            return make_response(jsonify({"success": "Simulation created", "runtime_id": runtime_id}), 201)

        except BadRequestException as bre:
            abort(400, {"error": bre.args})
        except InternalException as ie:
            abort(500, {"error": ie.args})
