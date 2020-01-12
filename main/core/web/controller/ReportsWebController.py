from flask import make_response, jsonify, request, abort, Response

from flask_restful import Resource
from flask_restful_swagger import swagger

from main.core.model.exceptions.BadRequestExceptions import BadRequestException
from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.infrastructure.MongoAdapter import MongoAdapter
from main.core.util.JSONEncoder import JSONEncoder


class ReportsWebController(Resource):

    @swagger.operation(
        notes='Get all stored reports.',
        responseMessages=[
            {
                "code": 200,
                "message": "List of stored reports."
            },
            {
                "code": 400,
                "message": "Error, Bad Request"
            }
        ]
    )
    def get(self):
        try:
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

        except BadRequestException as bre:
            abort(400, {"error": bre.args})