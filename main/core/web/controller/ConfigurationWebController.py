from flask_restful import Resource
from flask import request, abort, make_response, jsonify

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.service.infrastructure.ScenarioBuilder import ScenarioBuilder
from main.core.service.operations.OperationsController import OperationsController
from main.core.service.operations.ToplogyManager import TopologyManager
from main.core.service.infrastructure.TopologyBuilder import TopologyBuilder
from main.core.service.simulation.Simulator import Simulator


class ConfigurationWebController(Resource):

    def post(self):
        try:
            # Parsing topology elements
            tb = TopologyBuilder()
            topology = tb.instantiate_topology(request.json['topology'])
            topology_manager = TopologyManager(topology)

            # Parsing simulation scenario
            sb = ScenarioBuilder()
            scenario = sb.instantiate_scenario(request.json['scenario'])
            sim_env = sb.get_sim_environment()

            # Create simulation
            simulator = Simulator(sim_env, scenario, topology_manager)

            # Register and start simulation
            oc = OperationsController.get_instance()
            runtime_id = oc.register_simulation(simulator)

            return make_response(jsonify({"runtime_id": runtime_id}), 200)

        except BadRequestException as bre:
            abort(400, {"error": bre.args})
        except InternalException as ie:
            abort(500, {"error": ie.args})
