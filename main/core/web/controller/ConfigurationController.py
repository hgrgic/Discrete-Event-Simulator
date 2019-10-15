from flask_restful import Resource
from flask import request, abort

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.model.exceptions.InternalExceptions import InternalException
from main.core.service.operations.ProcessManager import ProcessManager
from main.core.service.topology.ToplogyManager import TopologyManager
from main.core.service.topology.TopologyBuilder import TopologyBuilder
from main.des.ing.simulation.ScenarioBuilder import ScenarioBuilder
from main.des.ing.simulation.Simulator import Simulator


class ConfigurationController(Resource):
    def get(self):
        return {'config': "get config"}

    def post(self):
        try:
            tb = TopologyBuilder()
            topology = tb.instantiate_topology(request.json['topology'])
            topology_manager = TopologyManager(topology)
            process_manager = ProcessManager(topology_manager)

            sb = ScenarioBuilder()
            scenario = sb.instantiate_scenario(request.json['scenario'])

            # simulator = Simulator(scenario, process_manager)
            # simulator.run_simulator()
        except BadRequestException as bre:
            abort(400, {"error": bre.args})
        except InternalException as ie:
            abort(500, {"error": ie.args})