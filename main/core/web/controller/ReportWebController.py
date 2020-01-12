from flask import make_response, jsonify, request, abort, Response

from flask_restful import Resource
from flask_restful_swagger import swagger

from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.infrastructure.MongoAdapter import MongoAdapter
from main.core.util.JSONEncoder import JSONEncoder


class ReportWebController(Resource):

    @swagger.operation(
        notes='Get report by runtime_id',
        parameters=[
            {
                "name": "runtime_id",
                "description": "Runtime ID of the simulation.",
                "required": True,
                "dataType": "String",
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Report with metrics from the completed simulation."
            },
            {
                "code": 404,
                "message": "Error, No report found."
            },
            {
                "code": 400,
                "message": "Error, Bad Request."
            }
        ]
    )
    def get(self):
        if request.args.get("runtime_id") is not None:
            # Open connection to database
            ma = MongoAdapter(authenticate=True)
            ma.open_db_connection()
            collection = ma.get_collection("reports")

            # Get report from db
            document = SimulationReport.get_report(request.args.get("runtime_id"), collection)
            ma.close_db_connection()

            if document is None:
                abort(404, {"error": "Document not found"})

            return Response(response=JSONEncoder().encode(document),
                            status=200,
                            mimetype="application/json")
        else:
            abort(400, {"error": "Expected runtime_id as query parameter"})

    @swagger.operation(
        notes='Delete a report from the database',
        parameters=[
            {"name": "runtime_id",
             "description": "Runtime ID of the report.",
             "required": True,
             "dataType": "String",
             "paramType": "query"
             }
        ],
        responseMessages=[
            {
                "code": 200,
                "message": "Document deleted."
            },
            {
                "code": 404,
                "message": "Error, No report found."
            },
            {
                "code": 400,
                "message": "Error, Bad Request."
            }
        ]
    )
    def delete(self):
        if request.args.get("runtime_id") is not None:
            # Open connection to db
            ma = MongoAdapter(authenticate=True)
            ma.open_db_connection()
            collection = ma.get_collection("reports")

            # Delete report from db
            count = SimulationReport.delete_report(request.args.get("runtime_id"), collection)
            ma.close_db_connection()
            if count != 1:
                abort(404, {"error": "Document possibly not deleted!"})
            return make_response({"success": "Document deleted"}, 200)

        abort(400, {"error": "Expected runtime_id as query parameter"})
