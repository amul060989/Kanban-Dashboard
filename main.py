import os
from flask import Flask
from application import config
from application.config import LocalDev
from application.database import db
from flask_restful import Resource,Api

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      # app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    else:
      # app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDev)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    # app.logger.info("App setup complete")
    return app,api

app,api = create_app()

# Import all the controllers so they are loaded
from application.controllers import *
from application.api import TaskAPI

api.add_resource(TaskAPI,"/api/<string:task_id>","/api/new_task")

if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',port=8080)
