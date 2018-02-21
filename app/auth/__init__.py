""" auth/__init__.py """

from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
auth = Blueprint('auth', __name__)

from . import views