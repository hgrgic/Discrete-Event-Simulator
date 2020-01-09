from flask import make_response, jsonify, request, abort, Response

from flask_restful import Resource

from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.infrastructure.MongoAdapter import MongoAdapter
from main.core.util.JSONEncoder import JSONEncoder


class ReportsWebController(Resource):

    def get(self):
        # Open connection to database
        ma = MongoAdapter(authenticate=True)
        ma.open_db_connection()
        collection = ma.get_collection("reports")

        # Get reports from db
        document = SimulationReport.get_reports(collection)
        ma.close_db_connection()

        return Response(response=document,
                        status=200,
                        mimetype="application/json")