from functools import wraps
from flask import render_template, request, session, jsonify
from flask_login import login_manager
from app import app, user_object, events_obj, eventdetails_obj

# Variable stores user's email
user = None


@app.route('/api/v1')
def index():
    # Render index page
    
    return jsonify({"message": "Welcome to Bright Events"})


@app.route('/api/v1/auth/register', methods=['GET', 'POST'])
def register():
    # User registeration
    
    if request.method == "POST":
            username = request.json['username']
            print(username)
            email = request.json['email']
            password = request.json['password']
            cpassword = request.json['cpassword']
                           
            msg = user_object.registerUser(username, email, password, cpassword)
            response = msg
            return response

@app.route('/api/v1/auth/login', methods=['GET', 'POST'])
def login():
    # User login
    
    if request.method == "POST":
            username = request.json['username']
            password = request.json['password']
            session['username']= username            
            msg = user_object.login(username, password)
            response = msg
            return response

@app.route('/api/v1/event', methods=['GET', 'POST'])
def event():
    # create event
    if request.method == "POST":
        event_name = request.json['event_name']
        user = request.json['user']
        category = request.json['category']
        location = request.json['location']
        date = request.json['date']

        msg = events_obj.createEvent(event_name, user, category, location, date)
        response = msg
        return jsonify(response)
    elif request.method == "GET":
        event = events_obj.allEvents()
        
        return jsonify(event)

@app.route('/api/v1/events/<eventId>', methods=['PUT'])
def edit_event(eventId):
    # edit event
    if request.method == "PUT":
        old_name = eventId
        edit_name = request.json['edit_name']
        user = request.json["username"]
        update_event = events_obj.editEvent(edit_name, old_name, user)
        return jsonify(update_event)
        # if == "" or update_event==""
        # register jsonify(mess = "")
        # eles:
        # jsonify({ mess = ",

        #    = update_event})

@app.route('/api/v1/event/<eventId>', methods=['DELETE'])
def delete_event(eventId):
    # delete event
    event_name = eventId
    user = session['username']
    delete = events_obj.deleteEvent(event_name, user)
    return jsonify(delete)
               

@app.route('/api/v1/event/<eventid>/rsvp', methods=['GET','POST'])
def rsvp(eventid):
	# Allowing a user to RSVP to an event
    if request.method == 'POST':
        event_name = eventid
        user = session['username']
        email = user_object.get_user_by_email(user)
            
        if not events_obj.get_event_by_name(event_name):
            return "Event does not exist"    
        print(user)        
        msg = eventdetails_obj.addGuest(event_name, user, email)
        print(msg)
        response = msg
        return response
    if request.method == 'GET':
        event_name = eventid
        visitors = eventdetails_obj.viewGuests(event_name)
        print(visitors)
        response = visitors
        return jsonify(response)

@app.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    #Reseting password
    if request.method == "POST":
        npassword = request.json['npassword']
        cpassword = request.json['cpassword']
        msg = user_object.changePassword(npassword,cpassword)
        return msg

@app.route('/api/v1/logout', methods=['POST'])
def logout():
    # Logging out
    new = session['username']
    if new:
        session.pop('username', None)
        return jsonify({"message": "Logout successful"})
    return jsonify({"message": "You are not logged in"})
        




	
