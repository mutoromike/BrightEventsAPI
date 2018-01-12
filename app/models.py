""" app/models.py 
    file to handle creation of models
"""

from app import db
from flask_bcrypt import Bcrypt

class User(db.Model):
    """
    Class defining user table
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128))
    email = db.Column(db.String(128))
    password = db.Column(db.String(256))

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

    def __init__(self, name, created_by):
        """
        Initialize an event with all its details
        """
        self.name = name
        self.category = category
        self.location = location
        self.date = date
        self.description = description
        self.created_by = created_by

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

