from flask_restful import Resource
from flask import request, abort

from main.core.model.exceptions.NoSuchTopologyElementException import NoSuchTopologyElementException
from main.core.service.topology.ToplogyManager import TopologyManager
from main.core.service.topology.TopologyBuilder import TopologyBuilder


class ConfigurationController(Resource):
    def get(self):
        return {'config': "get config"}

    def post(self):
        try:
            topology = TopologyBuilder.instantiate_topology(request.json['topology'])
            topology_manager = TopologyManager(topology)
            #TODO: pass topology manager to some DES manager
        except NoSuchTopologyElementException as nst:
            abort(400, {"error": nst.args})