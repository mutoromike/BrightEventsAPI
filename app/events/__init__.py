""" events/__init__.py """

from flask import Blueprint

# This instance of a Blueprint that represents the events blueprint
events = Blueprint('events', __name__)

from app.events import views