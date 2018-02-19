""" /app/auth/views.py """

from . import auth_blueprint

from flask.views import MethodView
from flask_bcrypt import Bcrypt
from flask import make_response, request, jsonify
from app.models import User, BlacklistToken
import re


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/register"""

        # Query to see if the user already exists
        req = request.get_json()
        user = User.query.filter_by(email=req['email']).first()
        user_name = User.query.filter_by(username=req['username']).first()
        
        username = req['username']
        email = req['email']
        password = req['password']
        cpassword = req['cpassword']

        if not user_name:
            # Username does not exist, try to register.
            if not user:
                # There is no user so we'll try to register them
                if re.match("^[a-zA-Z0-9_]*$", username):
                    # Check username special characters
                    if re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email):
                        # Check email validity
                        if (password==cpassword):
                            # Verify passwords are matching
                            if len(username)>5:
                                # Checkusername length
                                if len(req['password']) > 5 and re.search("[a-z]", req['password']) and\
                                re.search("[0-9]", req['password']) and re.search("[A-Z]", req['password']) \
                                and re.search("[$#@]", req['password']):
                                    try:
                                        # Register the user
                                        user = User(username=username, email=email, password=password)
                                        user.save()
                                        response = {
                                            'message': 'You registered successfully. Please log in.'
                                        }
                                        # return a response notifying the user that they registered successfully
                                            
                                    except Exception as e:
                                        # An error occured, therefore return a string message containing the error
                                        response = {
                                            'message': str(e)
                                        }
                                        return make_response(jsonify(response)), 401
                                    return make_response(jsonify(response)), 201

                                response = {
                                    'message': 'Password length should be more than 5 characters, '\
                                        'have one lowercase, uppercase, number and special character'
                                }
                                # return an error message if requirement not met
                                # 403 - failed authentication
                                return make_response(jsonify(response)), 403
                            response = {
                                'message': 'Username must be more than 5 characters'
                            }
                            # return an error message if requirement not met
                            # 403 - failed authentication
                            return make_response(jsonify(response)), 403
                        response = {
                            'message': 'The passwords should match!'
                        }
                        # return an error message, notifyin user to use matching passwords
                        # 403 - failed authentication
                        return make_response(jsonify(response)), 403

                    response = {
                        'message': 'Provide a valid email!'
                    }
                    # return an error message, notifyin user to use a valid username
                    return make_response(jsonify(response)), 400
                
                response = {
                    'message': 'Username cannot have special characters!'
                }
                # return an error message, notifyin user to use a valid username
                return make_response(jsonify(response)), 400
            
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202
        
        # Return a message to the user telling them that they they already exist
        response = {
            'message': 'Username already exists'
        }

        return make_response(jsonify(response)), 302

class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # Get the user object using their email (unique to every user)
            req = request.get_json()
            user = User.query.filter_by(email=req['email']).first()

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(req['password']):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

class PassReset(MethodView):
    """This class-based view handles user password resetting."""

    def put(self):
        """Handle POST request for this view. Url ---> /api/v2/auth/reset-password"""

        # get the access token from the authorization header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # User authenticated, proceed...
                # Get the user object using their id (unique to every user)                
                user = User.query.filter_by(id=user_id).first()
                req = request.get_json()
                npass = req['npassword']
                cpass = req['cnfpassword']
                print(npass)
                # Try to authenticate user id and password fields
                if user.id==user_id:
                    if npass==cpass:
                        try:
                            # Edit the password
                            user.password = Bcrypt().generate_password_hash(npass).decode()
                            user.save()
                            response = {
                                'message': 'Password changed successfully.'
                            }
                        except Exception as e:
                            # Create a response containing an string error message
                            response = {
                                'message': str(e)
                            }
                            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
                            return make_response(jsonify(response)), 500
                        return make_response(jsonify(response)), 200
                    
                    # Passwords aren't matching. Therefore, we return an error message
                    response = {
                        'message': 'Enter matching passwords'
                    }
                    return make_response(jsonify(response)), 400
                
                # Users can only edit their passwords
                response = {
                    'message': 'You can only edit your own password'
                }
                return make_response(jsonify(response)), 401
                		
            # user is not legit, so the payload is an error message
            message = user_id
            response = {
                'message': message
            }
            # return an error response, telling the user he is Unauthorized
            return make_response(jsonify(response)), 401    

class LogoutView(MethodView):
    """This class-based view handles user logout and access token blacklisting."""

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        access_token = auth_header

        if access_token:
            user_id = User.decode_token(access_token)
            # print(user_id)
            blacklisted = BlacklistToken.query.filter_by(token=access_token).first()
            if not blacklisted:
                if not isinstance(user_id, str):
                    # mark the token as blacklisted                
                    try:
                        # insert the token
                        blacklist_token = BlacklistToken(token=access_token)
                        blacklist_token.save()
                        response = {
                            'message': 'Successfully logged out.'
                        }
                        return make_response(jsonify(response)), 200
                    except Exception as e:
                        response = {
                            'message': e
                        }
                        return make_response(jsonify(response)), 200
                else:
                    response = {
                        'message': user_id
                    }
                    return make_response(jsonify(response)), 401
            else:
                response = {
                    'message': 'You were logged out! TOKEN EXPIRED!'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'Ivalid token'
            }
            return make_response(jsonify(response)), 403
                


registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
pass_reset = PassReset.as_view('pass_reset_veiw')
logout_view = LogoutView.as_view('logout_view')
# Define the rule for the registration url --->  /api/v2/auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v2/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the login url --->  /api/v2/auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v2/auth/login',
    view_func=login_view,
    methods=['POST']
)

# Define the rule for password reset --->  /api/v2/auth/reset-password
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v2/auth/reset-password',
    view_func=pass_reset,
    methods=['PUT']
)

# Define the rule for the logout url --->  /api/v2/auth/logout
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/api/v2/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
