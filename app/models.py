""" app/models.py 
    file to handle creation of models
"""

from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app

class User(db.Model):
    """
    Class defining user table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(256))
    events = db.relationship('Events', order_by='Events.id', cascade="all, delete-orphan")

    def __init__(self, username, email, password):
        """
        Initialization of user credentials
        """

        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """

        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """
        Save a user to the databse
        """

        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS512'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"



class Events(db.Model):
    """
    This class defines the events table
    """

    __tablename__ = 'events'

    # define the columns of the table, starting with its primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    category = db.Column(db.String(128))
    location = db.Column(db.String(128))
    date = db.Column(db.String(255))
    description = db.Column(db.String(16384))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    
    def save(self):
        """
        Save events,this applies for both creating a 
        new event and updating an existing one
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """
        This method gets all the events for a given user
        """
        return Events.query.filter_by(created_by=user_id)

    def delete(self):
        """
        Deletes a given event
        """
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Return a representation of an event instance
        """
        return "<Events: {}>".format(self.name)

    
