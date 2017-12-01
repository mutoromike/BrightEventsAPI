#app/__init__.py 

from flask import Flask
from app.useraccounts import UserClass
from app.events import EventsClass
from app.eventdetails import EventDetails


# Initialize the app
app = Flask(__name__, instance_relative_config=True)
app.secret_key = 'tonystarktheironman'

user_object = UserClass()
events_obj = EventsClass()
eventdetails_obj = EventDetails()

from app import views

# Load the config file
app.config.from_object('config')
