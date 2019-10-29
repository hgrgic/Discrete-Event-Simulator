from flask import Flask
from flask_restful import Api

from main.core.web.controller.ConfigurationWebController import ConfigurationWebController
from main.core.web.controller.SimulationWebController import SimulationController

app = Flask(__name__)
api = Api(app)

api.add_resource(ConfigurationWebController, '/config')
api.add_resource(SimulationController, '/simulation')

app.run(port='8080')

print ("APIs:", api.urls.values())