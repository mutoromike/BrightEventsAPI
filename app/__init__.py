""" app/__init__.py """

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
	from app.models import Events
	# Initialize app
	app = Flask(__name__, instance_relative_config=True)

	#load from config.py in root folder
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)	
	return app