from flask import Flask
app = Flask(__name__)

from main import core

from flask_restful import Api
from flask_restful_swagger import swagger

from main.core.web.controller.ReportsWebController import ReportsWebController
from main.core.web.controller.ReportWebController import ReportWebController
from main.core.web.controller.SimulationWebController import SimulationWebController
from main.core.web.controller.SimulationsWebController import SimulationsWebController


api = swagger.docs(Api(app), apiVersion='0.1',
                   description='ING Discrete Event Simulator',
                   api_spec_url='/docs',
                   basePath='http://localhost:8080')

api.add_resource(SimulationWebController, '/simulation')
api.add_resource(SimulationsWebController, '/simulations')
api.add_resource(ReportWebController, '/report')
api.add_resource(ReportsWebController, '/reports')