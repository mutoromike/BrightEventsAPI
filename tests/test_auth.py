""" /tests/test_auth.py """

import unittest
import json
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        # initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_data = {
            'username':'chrisevans',
            'email': 'test@example.com',
            'password': 'J@yd33n',
            'cpassword': 'J@yd33n'
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'J@yd33n'
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, data):
        return self.client().post('api/v2/auth/register', data=json.dumps(data), content_type='application/json' )

    def login_user(self, data):
        return self.client().post('/api/v2/auth/login', data=json.dumps(data), content_type='application/json' )
        
    def test_registration(self):
        """Test user registration works correcty."""
        res = self.register_user(self.user_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "You registered successfully. Please log in.")
        self.assertEqual(res.status_code, 201)
    
    def test_username_characters(self):
        """Test username registration special characters."""
        reg_data = {
                    'username':'chris# evans',
                    'email': 'test@example.com',
                    'password': 'J@yd33n',
                    'cpassword': 'J@yd33n'
                }

        res = self.register_user(reg_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "Username cannot have special characters!")
        self.assertEqual(res.status_code, 403)

    def test_email_validity(self):
        """Test email registration validity."""
        reg_data = {
                    'username':'chrisevans',
                    'email': 'test@examplecom',
                    'password': 'J@yd33n',
                    'cpassword': 'J@yd33n'
                }

        res = self.register_user(reg_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "Provide a valid email!")
        self.assertEqual(res.status_code, 403)

    def test_password_mismatch(self):
        """Test if passwords are matching."""
        reg_data = {
                    'username':'chrisevans',
                    'email': 'test@example.com',
                    'password': 'J@yd33n',
                    'cpassword': 'J@yd33na'
                }

        res = res = self.register_user(reg_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains an error message and a 403 status code
        self.assertEqual(result['message'], "The passwords should match!")
        self.assertEqual(res.status_code, 403)

    def test_username_length(self):
        """Test username length."""
        reg_data = {
                    'username':'csi',
                    'email': 'test@example.com',
                    'password': 'J@yd33n',
                    'cpassword': 'J@yd33n'
                }

        res = self.register_user(reg_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains an error message and a 403 status code
        self.assertIn("Username must be more than 5 characters", result['message'])
        self.assertEqual(res.status_code, 403)

    def test_password_strength(self):
        """Test if password is strong."""
        reg_data = {
                    'username':'chrisevans',
                    'email': 'test@example.com',
                    'password': 'badpassword',
                    'cpassword': 'badpassword'
                }

        res = self.register_user(reg_data)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains an error message and a 403 status code
        self.assertIn("Password length should be more than 5 characters", result['message'])
        self.assertEqual(res.status_code, 403)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        reg_data = {
                    'username':'chris',
                    'email': 'test@example.com',
                    'password': 'J@yd33n',
                    'cpassword': 'J@yd33n'
                }
        self.register_user(self.user_data)
        res = self.register_user(reg_data)
        self.assertEqual(res.status_code, 199)

    def test_already_existing_username(self):
        """Test if username already exists."""
        reg_data = {
                    'username':'chrisevans',
                    'email': 'test1@example.com',
                    'password': 'J@yd33n',
                    'cpassword': 'J@yd33n'
                }

        self.register_user(self.user_data)
        res = self.register_user(reg_data)
        self.assertEqual(res.status_code, 302)
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains the error message
        self.assertEqual(result['message'], "Username already exists")

    def test_user_login(self):
        """Test registered user can login."""
        
        res = self.register_user(self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.login_user(self.login_data)

        # get the results in json format
        result = json.loads(login_res.data.decode())
        # Test that the response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")
        # Assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_invalid_user_login(self):
        """Test non registered users cannot login."""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'J@yd33n'
        }
        # send a POST request to /auth/login with the data above
        res = self.login_user(not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())
        # assert that this response must contain an error message
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again")
   
    def test_successful_pass_editing(self):
        """Test successful password editing."""
        # Create a user
        res = self.register_user(self.user_data)
        self.assertEqual(res.status_code, 201)
        # Get token        
        access_token = self.get_token()
        # define a dictionary to represent the new passwords
        edit_password = {
            'npassword': 'J@yd33n56',
            'cnfpassword': 'J@yd33n56'
        }
        # send a PUT request to /api/v2/auth/reset-password with the data above
        res = self.client().put('/api/v2/auth/reset-password', headers=dict(Authorization= access_token), \
        data=json.dumps(edit_password), content_type='application/json')
        # get the result in json
        result = json.loads(res.data.decode())

        # assert that this response is successful 
        # and a success status code 200(ok)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            result['message'], "Password changed successfully.")

    def get_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data)
        result = self.login_user(self.login_data)
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def test_successful_logout(self):
        """Test if a user can successfully logout"""
        # Get token
        access_token = self.get_token()
        # Logout user
        res = self.client().post('/api/v2/auth/logout', headers=dict(Authorization=access_token),
        content_type='application/json')
        self.assertEqual(res.status_code, 200)
        result = json.loads(res.data.decode())
        self.assertIn('Successfully logged out.', result['message'])

    def test_repeat_logout(self):
        """Test if a user is prevented to logout twice"""
        # Get token
        access_token = self.get_token()        
        # Logout user
        self.client().post('/api/v2/auth/logout', headers=dict(Authorization=access_token),
        content_type='application/json')
        res = self.client().post('/api/v2/auth/logout', headers=dict(Authorization=access_token),
        content_type='application/json')     
        self.assertEqual(res.status_code, 401)
        result = json.loads(res.data.decode())
        self.assertIn('Logged out. Please', result['message'])