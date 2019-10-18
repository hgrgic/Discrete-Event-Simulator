from flask_restful import Resource
from flask import request, abort

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.service.topology.ToplogyManager import TopologyManager
from main.core.service.topology.TopologyBuilder import TopologyBuilder
from main.des.ing.simulation.SimulationBuilder import SimulationBuilder
from main.des.ing.simulation.Simulator import Simulator


class ConfigurationController(Resource):
    def get(self):
        return {'config': "get config"}

    def post(self):
        try:
            # Parsing topology elements
            tb = TopologyBuilder()
            topology = tb.instantiate_topology(request.json['topology'])
            topology_manager = TopologyManager(topology)

            # Parsing simulation scenario
            sb = SimulationBuilder()
            scenario = sb.instantiate_scenario(request.json['scenario'])
            sim_env = sb.get_sim_environment()

            # Starting simulation
            simulator = Simulator(sim_env, scenario, topology_manager)
            simulator.start_simulation()

        except BadRequestException as bre:
            abort(400, {"error": bre.args})
        except InternalException as ie:
            abort(500, {"error": ie.args})
