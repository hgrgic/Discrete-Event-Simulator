from multiprocessing import Process
from threading import Thread

from flask_restful import Resource
from flask import request, abort, make_response, jsonify

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.service.infrastructure.ScenarioBuilder import ScenarioBuilder
from main.core.service.operations.OperationsController import OperationsController
from main.core.service.operations.ToplogyManager import TopologyController
from main.core.service.infrastructure.TopologyBuilder import TopologyBuilder
from main.core.service.simulation.Simulator import Simulator


class ConfigurationWebController(Resource):

    def post(self):
        try:
            # Parsing topology elements
            tb = TopologyBuilder()
            topology = tb.instantiate_topology(request.json['topology'])
            topology_controller = TopologyController(topology)

            # Parsing simulation scenario
            sb = ScenarioBuilder()
            scenario = sb.instantiate_scenario(request.json['scenario'])
            sim_env = sb.get_sim_environment()

            # Create simulation
            simulator = Simulator(sim_env, scenario, topology_controller)

            # Register and start simulation
            oc = OperationsController.get_instance()
            thread = Thread(target=oc.register_simulation, args=(simulator,))
            thread.start()

            return make_response(jsonify({"success": "Simulation created"}), 201)

        except BadRequestException as bre:
            abort(400, {"error": bre.args})
        except InternalException as ie:
            abort(500, {"error": ie.args})
