""" app/__init__.py """

from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
	from app.models import Events
	"""
	Initialize app
	"""
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	@app.route('/api/v2/events', methods=['POST', 'GET'])
	def events():
		if request.method == "POST":
			event = request.get_json()
			print(event)
			created_event = Events(
									name=event['name'], 
									category=event['category'], 
									location=event['location'], 
									date=event['date'], 
									description=event['description']
									)
			created_event.save()
			response = jsonify({
				'id': 'created_event.id',
				'name' : 'name',
				'category' : 'category',
				'location' : 'location',
				'date' : 'date',
				'description' : 'description'
			})
			response.status_code = 201
			return response
		else:
			""" 
			GET
			"""
			user_id = 1
			events = Events.get_all(user_id)
			results = []

			for event in events:
				obj = {
					'id': event.id,
					'name' : name,
					'category' : category,
					'location' : location,
					'date' : date,
					'description' : description
				}
				results.append(obj)
			response = jsonify(results)
			response.status_code = 200
			return response

	from .auth import auth_blueprint
	app.register_blueprint(auth_blueprint)

	return app