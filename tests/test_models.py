"""
File to handle testing of the created models
"""

import unittest
from flask import jsonify
import os
import json
from app import create_app, db

class EventsTestCase(unittest.TestCase):
    """
    This class represents the events test case
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.event = {'name': 'birthday', 'category': 'party', 'location': 'nairobi', 'date': '12/12/2018',\
        'description': 'Everyone is welcome'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, username ="chrisevans", email = "test@example.com",
                     password = "test_password"):
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }
        return self.client().post('/auth/register', data=json.dumps(user_data), content_type='application/json' )

    def login_user(self, email="test@example.com", password="test_password"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/auth/login', data=json.dumps(user_data), content_type='application/json' )

    def get_token(self):
        """register and login a user to get an access token"""
        self.register_user()
        result = self.login_user()
        # self.assertIn('You logged in successfully.', str(result))
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def test_event_creation(self):
        """
        Test if API can create an event (POST request)    
        """
        access_token = self.get_token()  

        result = self.client().post('/api/v2/event', headers=dict(Authorization=access_token), 
            data=json.dumps(self.event), content_type='application/json' )
        self.assertEqual(result.status_code, 201)
        self.assertEqual(self.event['name'], 'birthday')

    def test_getting_all_events(self):
        """
        Test API can get an Event (GET request).
        """
        access_token = self.get_token()

        # create an event by making a POST request
        res = self.client().post(
            '/api/v2/event',
            headers=dict(Authorization= access_token), 
            data=json.dumps(self.event), content_type='application/json')
        self.assertEqual(res.status_code, 201)

        # get all the event that belong to the test user by making a GET request
        res = self.client().get(
            '/api/v2/event',
            headers=dict(Authorization= access_token),
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.event['name'], 'birthday')

    def test_get_event_by_id(self):
        """Test API can get a single event by using it's id."""
        access_token = self.get_token()

        req = self.client().post(
            '/api/v2/event',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')

        # assert that the event is created 
        self.assertEqual(req.status_code, 201)
        # get the response data in json format
        results = json.loads(req.data.decode())

        result = self.client().get(
            '/api/v2/event/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        # assert that the event is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertEqual(self.event['name'], 'birthday')

    def test_event_editing(self):
        """Test API can edit an existing event. (PUT request)"""
        access_token = self.get_token()
        # Create an event
        req = self.client().post(
            '/api/v2/event',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        self.assertEqual(req.status_code, 201)
        
        results = json.loads(req.data.decode())

        # Edit created event
        edit={
                "name": "Software",
                'category' : 'Development',
                'location' : 'Eldoret',
                'date' : '12/1/2019',
                'description' : 'Prizes will be won'
            }
        req = self.client().put(
            '/api/v2/event/{}'.format(results['id']),
            headers=dict(Authorization= access_token),
            data=json.dumps(edit), content_type='application/json')
        self.assertEqual(req.status_code, 200)

        # Get the edited event
        results = self.client().get(
            '/api/v2/event/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        self.assertIn("Software", str(results.data))

    def test_deleting_of_event(self):
        """Test API can delete an existing Event. (DELETE request)."""
        access_token = self.get_token()

        req = self.client().post(
            '/api/v2/event',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        self.assertEqual(req.status_code, 201)
        results = json.loads(req.data.decode())

        # Delete created event
        res = self.client().delete(
            '/api/v2/event/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/api/v2/event/1',
            headers=dict(Authorization= access_token))
        self.assertEqual(result.status_code, 404)

    def test_successful_rsvp(self):
        """Test API can create successful rsvp."""
        access_token = self.get_token()
        # Create event
        req = self.client().post(
            '/api/v2/event',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        self.assertEqual(req.status_code, 201)

        results = json.loads(req.data.decode())
        # RSVP to event
        res = self.client().post('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('RSVP Successful', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
    

if __name__ == "__main__":
    unittest.main()