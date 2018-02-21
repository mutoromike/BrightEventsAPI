"""
File to handle testing of event details.
"""

import unittest
from flask import jsonify
import json
from app import create_app, db

class MoreEventsTestCase(unittest.TestCase):
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
        self.user_data = {'username': "chrisevans", 'email': "test@example.com", 'password': "J@yd33n",
            'cpassword': "J@yd33n"}
        self.login_data = {'email': "test@example.com", 'password': "J@yd33n"}
        self.user_data2 = {'username': "brucebarner", 'email': "bruce@infinity.com",
            'password': "sTr0ng3st@venger", 'cpassword': "sTr0ng3st@venger"}
        self.login_data2 = {'email': "bruce@infinity.com", 'password': "sTr0ng3st@venger"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, data):
        return self.client().post('api/v2/auth/register', data=json.dumps(data), content_type='application/json' )

    def login_user(self, data):
        return self.client().post('/api/v2/auth/login', data=json.dumps(data), content_type='application/json' )

    def get_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data)
        result = self.login_user(self.login_data)
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def get_new_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data2)
        result = self.login_user(self.login_data2)
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def test_successful_rsvp(self):
        """Test API can create successful rsvp."""
        access_token = self.get_token()
        # Create event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # RSVP to event
        res = self.client().post('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('RSVP Successful', str(res.data))
    
    def test_logged_out_rsvp(self):
        """Test API can prevent a logged out user from rsvp"""
        access_token = self.get_token()
        # Create event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # RSVP to event
        self.client().post('/api/v2/auth/logout', headers=dict(Authorization=access_token),
        content_type='application/json')
        res = self.client().post('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token),
            content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn('Logged out.', str(res.data))

    def test_double_rsvp(self):
        """Test API can capture double rsvp."""
        access_token = self.get_token()
        # Create event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # RSVP to event
        res = self.client().post('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertIn('RSVP Successful', str(res.data))

        # Repeat RSVP to event
        res = self.client().post('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token),
            content_type='application/json')
        self.assertEqual(res.status_code, 302)
        self.assertIn('Reservation already created!', str(res.data))

    def test_successful_view_rsvp(self):
        """Test successful return of rsvp list"""
        access_token = self.get_token()
        # Create event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # RSVP to event
        res = self.client().post('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token),
            content_type='application/json')

        # Get list of RSVP to event
        res = self.client().get('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)


    def test_view_rsvp(self):
        """Test User can only view rsvp list of their own event"""
        access_token = self.get_token()
        access_token2 = self.get_new_token()
        # Create event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # RSVP to event
        res = self.client().post('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token2),
            content_type='application/json')

        # Get list of RSVP to event
        res = self.client().get('/api/v2/event/{}/rsvp'.format(results['id']),
            headers=dict(Authorization= access_token2),
            content_type='application/json')
        self.assertEqual(res.status_code, 401)
        self.assertIn('You can only see visitors ', str(res.data))

    def test_creation_of_similar_event(self):
        """
        Test API can skip creation of similar event.
        """
        access_token = self.get_token()

        # create an event by making a POST request
        self.client().post('/api/v2/events',
            headers=dict(Authorization= access_token), 
            data=json.dumps(self.event), content_type='application/json')

        # Create a similar event and check the error
        myevent = {'name': 'birthday', 'category': 'party', 'location': 'nairobi', 'date': '12/12/2018',\
        'description': 'Everyone is welcome'}
        result = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token), 
            data=json.dumps(myevent), content_type='application/json')
        self.assertEqual(result.status_code, 302)

    def test_search_by_location(self):
        """
        Test API can search events by location (GET request).
        """
        access_token = self.get_token()

        # create an event by making a POST request
        res = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token), 
            data=json.dumps(self.event), content_type='application/json')
        # get all the event that belong to the test user by making a GET request
        res = self.client().post('/api/v2/search',
            data=json.dumps({'location': 'nairobi'}), content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_search_by_category(self):
        """
        Test API can search events by category (GET request).
        """
        access_token = self.get_token()

        # create an event by making a POST request
        res = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token), 
            data=json.dumps(self.event), content_type='application/json')

        # get all the event that belong to the test user by making a GET request
        res = self.client().post('/api/v2/search',
            data=json.dumps({'category': 'party'}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
    
    def test_search_case_sensitivity(self):
        """
        Test that searching is case insensitive.
        """
        access_token = self.get_token()

        # create an event by making a POST request
        res = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token), 
            data=json.dumps(self.event), content_type='application/json')

        # get all the event that belong to the test user by making a GET request
        res = self.client().post('/api/v2/search',
            data=json.dumps({'category': 'PARty'}), content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_searching_non_existing_event(self):
        """
        Test searching of an event that does not exist.
        """
        # get all the event that belong to the test user by making a GET request
        res = self.client().post('/api/v2/search?category=learn', content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        # drop all tables
        db.session.remove()
        db.drop_all()    

if __name__ == "__main__":
    unittest.main()