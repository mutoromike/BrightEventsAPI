""" app/__init__.py """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config
import re

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
	# Initialize app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	from .auth import auth
	from .events import events
	app.register_blueprint(auth)
	app.register_blueprint(events)

	return app