from flask_restful import Resource
from flask import request, abort, jsonify

from main.core.model.exceptions.NoSuchTopologyElementException import NoSuchTopologyElementException
from main.core.service.topology.TopologyBuilder import TopologyBuilder


class ConfigurationController(Resource):
    def get(self):
        return {'config': "get config"}

    def post(self):
        try:
            builder = TopologyBuilder()
            builder.instantiate_topology(request.json['topology'])
        except NoSuchTopologyElementException as nst:
            abort(400, nst)