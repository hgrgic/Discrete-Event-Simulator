from flask import Flask
from flask_restful import Api

from main.core.web.controller.ReportsWebController import ReportsWebController
from main.core.web.controller.SimulationWebController import SimulationController

app = Flask(__name__)
api = Api(app)

api.add_resource(SimulationController, '/simulation')
api.add_resource(ReportsWebController, '/reports')

if __name__ == '__main__':
    app.run(port='8080')