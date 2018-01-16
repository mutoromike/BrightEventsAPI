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

    def test_event_creation(self):
        """
        Test if API can create an event (POST request)    
        """
        data = {
                    "name":"birthday",
                    "category":"party",
                    "location":"nairobi",
                    "date":"12/12/2018",
                    "description":"Everyone is attending"
                    }

        res = self.client().post('/api/v2/events', data=json.dumps(self.event), content_type='application/json' )
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['name'], 'birthday')

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()