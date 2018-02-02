""" app/__init__.py """

from flask import Flask, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from config import app_config
import re

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
	from app.models import Events, User
	"""
	Initialize app
	"""
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(app_config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	db.init_app(app)

	@app.route('/api/v2/events', methods=['POST', 'GET'])
	@app.route('/api/v2/events/page=<int:page>', methods=['GET'])
	def events(page=1):

		# Get the access token from the header
		auth_header = request.headers.get('Authorization')
		access_token = auth_header

		if access_token:
         # Attempt to decode the token and get the User ID
			user_id = User.decode_token(access_token)
			if not isinstance(user_id, str):
				# Go ahead and handle the request, the user is authenticated
				current_user = User.query.filter_by(id=user_id).first()

				if request.method == "POST":
					event = request.get_json()
					name=event['name'], 
					category=event['category'], 
					location=event['location'], 
					date=event['date'], 
					description=event['description']
					if name is None or category is None or location is None:
						# Check whether fields are not empty												
						response = {"message" : "Event details cannot be empty!"}
						return make_response(jsonify(response)), 400
					# if not re.match("^[a-zA-Z0-9_]*$", name):
					# 	response = {"message" : "Event name cannot have special characters!"}
					# 	return make_response(jsonify(response)), 400
					existing=Events.query.filter_by(name=name).filter_by(category=category).filter_by\
					(created_by=user_id).first()					
					print(current_user.events)
					if existing:
						response = {"message" : "A similar event already exists!"}
						return make_response(jsonify(response)), 302					
					try:
						created_event = Events(
										name=name, 
										category=category, 
										location=location, 
										date=date, 
										description=description,
										created_by = user_id
										)
						created_event.save()
						response = jsonify({
							'id': created_event.id,
							'name' : created_event.name,
							'category' : created_event.category,
							'location' : created_event.location,
							'date' : created_event.date,
							'description' : created_event.description,
							'created_by' : created_event.created_by
						})
							

					except AttributeError:
						response = {"message": "There was an error creating the event, please try again"}
						return make_response(jsonify(response)), 500
					return make_response(response), 201

				else:
					""" 
					GET
					"""
					events = Events.query.filter_by(created_by=user_id).paginate(page, per_page = 3, error_out=True).items
					# Query all
					# events = Events.query.paginate(page, per_page = 3, error_out=True).items
					# events = Events.get_all(user_id)
					results = []

					for event in events:
						obj = {
							'id': event.id,
							'name' : event.name,
							'category' : event.category,
							'location' : event.location,
							'date' : event.date,
							'description' : event.description

						}
						results.append(obj)

					return make_response(jsonify(results)), 200
			
			else:
				# user is not legit, so the payload is an error message
				message = user_id
				response = {
					'message': message
				}
				return make_response(jsonify(response)), 401

	@app.route('/api/v2/events/<int:id>', methods=['GET', 'PUT', 'DELETE'])
	def event_tasks(id, **kwargs):
		# get the access token from the authorization header
		auth_header = request.headers.get('Authorization')
		access_token = auth_header

		if access_token:
			# Get the user id related to this access token
			user_id = User.decode_token(access_token)

			if not isinstance(user_id, str):
				# If the id is not a string(error), we have a user id
				# Get the event with the id specified from the URL (<int:id>)
				event = Events.query.filter_by(id=id).first()
				# print(event)
				if not event:
					# There is no event with this ID for this User, so
					# Raise an HTTPException with a 404 not found status code
					abort(404)

				if request.method == "DELETE":
					# delete the event using our delete method
					event.delete()
					response = {
						"message": "event {} deleted".format(event.id)
					}

					return jsonify(response), 200

				elif request.method == 'PUT':
					# Obtain the new name of the bucketlist from the request data
					edited = request.get_json()

					event.name=edited['name']
					event.category=edited['category']
					event.location=edited['location']
					event.date=edited['date']
					event.description=edited['description']
					event.save()

					response = {
						'id': event.id,
						'name' : event.name,
						'category' : event.category,
						'location' : event.location,
						'date' : event.date,
						'description' : event.description
					}
					
					return make_response(jsonify(response)), 200
				else:
					# Handle GET request, sending back the event to the user
					response = {
						'id': event.id,
						'name' : event.name,
						'category' : event.category,
						'location' : event.location,
						'date' : event.date,
						'description' : event.description
					}
					return make_response(jsonify(response)), 200
			else:
				# user is not legit, so the payload is an error message
				message = user_id
				response = {
					'message': message
				}
				# return an error response, telling the user he is Unauthorized
				return make_response(jsonify(response)), 401

	@app.route('/api/v2/event/<event_id>/rsvp', methods=['POST', 'GET'])
	def rsvp(event_id):
		"""RSVP to an event"""
		# get the access token from the authorization header
		auth_header = request.headers.get('Authorization')
		access_token = auth_header
		if access_token:
			# Get the user id related to this access token
			user_id = User.decode_token(access_token)

			if not isinstance(user_id, str):
				# If the id is not a string(error), we have a user id
				# Get the event with the id specified from the URL (<int:id>)
				event = Events.query.filter_by(id=event_id).first()
				if event:
					# Check to see if event exists					
					if request.method == 'POST':
						current_user = User.query.filter_by(id=user_id).first()
						print(current_user)
						result = event.create_reservation(current_user)
						print(result)
						if result == "Reservation Created":
							return jsonify({"message" : "RSVP Successful"}), 201
						return jsonify({"message" : "Reservation already created!"}), 302

					guests = event.rsvp.all()

					if guests:
						attending_visitors = []
						for user in guests:
							new= {
								"username" : user.username,
								"email" : user.email
							}
							attending_visitors.append(new)
						return make_response(jsonify(attending_visitors)), 200

					response = {"message" : "No visitors"}
					return make_response(jsonify(response)), 200

				else:
					response = {"message" : "Event does not exist!"}
					return make_response(jsonify(response)), 404
			else:
				response = {"message" : "UNAUTHORIZED! Please login or sign up!"}
				return make_response(jsonify(response)), 401

	from .auth import auth_blueprint
	app.register_blueprint(auth_blueprint)

	return app