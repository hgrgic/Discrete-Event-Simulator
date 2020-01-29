from flask import make_response, request, abort, Response
from flask_restful import Resource
from flask_restful_swagger import swagger

from main.core.model.simulation.SimulationReport import SimulationReport
from main.core.service.infrastructure.MongoAdapter import MongoAdapter
from main.core.util.JSONEncoder import JSONEncoder

import pandas as pd


class ReportCsvWebController(Resource):

    @swagger.operation(
        notes='Get report in CSV format.',
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
                "message": "CSV of stored report."
            },
            {
                "code": 400,
                "message": "Error, Bad Request"
            }
        ]
    )
    def get(self):
        if request.args.get("runtime_id") is not None:
            # Open connection to database
            ma = MongoAdapter()
            ma.open_db_connection()
            collection = ma.get_collection("reports")

            # Get report from db
            document = SimulationReport.get_report(request.args.get("runtime_id"), collection)
            ma.close_db_connection()

            if document is None:
                abort(404, {"error": "Document not found"})
            else:
                df = pd.DataFrame(columns=["Step", "CPU Usage", "Queue", "Label", "Name", "Server", "ServerType"])
                for server in document['report']:
                    for component in server['metrics']:
                        metrics = pd.DataFrame(server['metrics'][component], columns=["Step", "CPU Usage", "Queue", "Label", "Name"])
                        metrics['Component'] = [component] * len(server['metrics'][component])
                        metrics['Server'] = [server['name']] * len(server['metrics'][component])
                        metrics['ServerType'] = [server['type']] * len(server['metrics'][component])
                        df = df.append(metrics)

                resp = make_response(df.to_csv(index=False))
                resp.headers["Content-Disposition"] = 'attachment; filename={}_{}_export.csv'.format(document['simulation_name'], document['runtime_id'])
                resp.headers["Content-Type"] = "text/csv"
                return resp
        else:
            abort(400, {"error": "Expected runtime_id as query parameter"})
