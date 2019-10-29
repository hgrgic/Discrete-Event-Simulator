from flask import make_response, jsonify, request, abort, Response

from flask_restful import Resource

from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.infrastructure.MongoAdapter import MongoAdapter
from main.core.util.JSONEncoder import JSONEncoder


class ReportsWebController(Resource):

    def get(self):
        if request.args.get("runtime_id") is not None:
            ma = MongoAdapter(authenticate=True)
            ma.open_db_connection()
            collection = ma.get_collection("reports")
            document = SimulationReport.get_report(request.args.get("runtime_id"), collection)
            ma.close_db_connection()

            if document is None:
                return make_response(jsonify({"message": "Document not found"}), 404)

            return Response(response=JSONEncoder().encode(document),
                            status=200,
                            mimetype="application/json")

        return make_response(jsonify({"error": "runtime_id expected as query parameter"}), 400)
