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
            'password': 'test_password',
            'cpassword': 'test_password'
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """Test user registration works correcty."""
        data = {
                    'username':'chrisevans',
                    'email': 'test@example.com',
                    'password': 'test_password',
                    'cpassword': 'test_password'
                }

        res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "You registered successfully. Please log in.")
        self.assertEqual(res.status_code, 201)
    
    def test_username_characters(self):
        """Test username registration special characters."""
        data = {
                    'username':'chris# evans',
                    'email': 'test@example.com',
                    'password': 'test_password',
                    'cpassword': 'test_password'
                }

        res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "Username cannot have special characters!")
        self.assertEqual(res.status_code, 400)

    def test_email_validity(self):
        """Test email registration validity."""
        data = {
                    'username':'chrisevans',
                    'email': 'test@examplecom',
                    'password': 'test_password',
                    'cpassword': 'test_password'
                }

        res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "Provide a valid email!")
        self.assertEqual(res.status_code, 400)

    def test_password_mismatch(self):
        """Test if passwords are matching."""
        data = {
                    'username':'chrisevans',
                    'email': 'test@example.com',
                    'password': 'test_password',
                    'cpassword': 'testpassword'
                }

        res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains an error message and a 403 status code
        self.assertEqual(result['message'], "The passwords should match!")
        self.assertEqual(res.status_code, 403)

    def test_username_and_and_pass(self):
        """Test if passwords are matching."""
        data = {
                    'username':'csi',
                    'email': 'test@example.com',
                    'password': 'testpass',
                    'cpassword': 'testpass'
                }

        res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        # get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains an error message and a 403 status code
        self.assertIn("Username and password must be more than", result['message'])
        self.assertEqual(res.status_code, 403)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        data = {
                    'username':'chris',
                    'email': 'test@example.com',
                    'password': 'test_password',
                    'cpassword': 'test_password'
                }
        res = self.client().post('/api/v2/auth/register', data=json.dumps(self.user_data), content_type='application/json' )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        self.assertEqual(second_res.status_code, 202)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please login.")

    def test_already_existing_username(self):
        """Test if username already exists."""
        data = {
                    'username':'chrisevans',
                    'email': 'test1@examplecom',
                    'password': 'test_password',
                    'cpassword': 'test_password'
                }

        res = self.client().post('/api/v2/auth/register', data=json.dumps(self.user_data), content_type='application/json' )
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        self.assertEqual(second_res.status_code, 302)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        # assert that the request contains the error message
        self.assertEqual(result['message'], "Username already exists")

    def test_user_login(self):
        """Test registered user can login."""
        data = {
                    'username':'chrisevans',
                    'email': 'test@example.com',
                    'password': 'test_password',
                    'cpassword': 'test_password'
                }

        data2 = {
                    'email': 'test@example.com',
                    'password': 'test_password'
                }
        res = self.client().post('/api/v2/auth/register', data=json.dumps(data), content_type='application/json' )
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/api/v2/auth/login', data=json.dumps(data2), content_type='application/json')

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
            'password': 'nope'
        }
        # send a POST request to /auth/login with the data above
        res = self.client().post('/api/v2/auth/login', data=json.dumps(not_a_user), content_type='application/json')
        # get the result in json
        result = json.loads(res.data.decode())

        # assert that this response must contain an error message 
        # and an error status code 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again")

    def login_user(self, email="test@example.com", password="test_password"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v2/auth/login', data=json.dumps(user_data), content_type='application/json' )

    def get_token(self):
        """register and login a user to get an access token"""
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def test_successful_pass_editing(self):
        """Test successful password editing."""
        # Create a user
        res = self.client().post('/api/v2/auth/register', data=json.dumps(self.user_data), content_type='application/json' )
        self.assertEqual(res.status_code, 201)
        # Get token        
        access_token = self.get_token()       
        # define a dictionary to represent the new passwords
        edit_password = {
            'npassword': 'ulembaya',
            'cnfpassword': 'ulembaya'
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

    