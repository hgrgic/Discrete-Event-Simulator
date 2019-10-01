from flask import Flask
from flask_restful import Api

from main.core.web.controller.ConfigurationController import ConfigurationController

app = Flask(__name__)
api = Api(app)


api.add_resource(ConfigurationController, '/config')

if __name__ == '__main__':
    app.run(port='8080')
