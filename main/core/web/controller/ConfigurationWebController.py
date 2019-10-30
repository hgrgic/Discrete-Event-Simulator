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
from main.core.util.IdentityUtility import get_unique_id


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
            runtime_id = get_unique_id()
            thread = Thread(target=oc.register_simulation, args=(simulator, runtime_id,))
            thread.start()

            return make_response(jsonify({"success": "Simulation created", "runtime_id": runtime_id}), 201)

        except BadRequestException as bre:
            abort(400, {"error": bre.args})
        except InternalException as ie:
            abort(500, {"error": ie.args})
