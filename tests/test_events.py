# Test events
import unittest
from app.events import EventsClass


class TestCasesEvents(unittest.TestCase):
    # Test for special character in event names
    # Test for owner of events
    # Test for correct output(event creation)
    # Test for deletion of existing event
    # Test for editing event names
    

    def setUp(self):
        # Setting up EventsClass
        
        self.events_class_obj = EventsClass()

    def tearDown(self):
        # Removing EventsClass
        
        del self.events_class_obj
    
    def test_special_characters(self):
        # Check for special characters in event name
        
        user = "mike@gmail.com"
        msg = self.events_class_obj.createEvent("Back.to-School", "soft*%ware", "nairo@&", "23/23/23", user)
        self.assertEqual(msg, "No special characters (. , ! space [] )")

    def test_return_of_all_events(self):
        # Check for all events in the system
        self.events_class_obj.events_list = [{'owner': 'mike@gmail.com', 'name': 'TeccDay', 'category': 'Software', 
                                                'location': 'Nairobi', 'date': '21/3/2017'},
                                                 {'owner': 'boris@gmail.com','name': 'Eatery', 'category': 'Food', 
                                                'location': 'Nairobi', 'date': '21/3/2017'}]
        msg = self.events_class_obj.events_list

        value = self.events_class_obj.allEvents() 
        self.assertEqual(msg, value)                                 
    
    def test_owner(self):
        # Check for events belonging to owner
        self.events_class_obj.events_list = [{'owner': 'mike@gmail.com', 'name': 'TeccDay', 'category': 'Software', 
                                                'location': 'Nairobi', 'date': '21/3/2017'},
                                                 {'owner': 'boris@gmail.com','name': 'Eatery', 'category': 'Food', 
                                                'location': 'Nairobi', 'date': '21/3/2017'}]
        user = "mike@gmail.com"
        msg = self.events_class_obj.getOwner(user)
        self.assertEqual(msg, [{'owner': 'mike@gmail.com', 'name': 'TeccDay', 'category': 'Software', 
                                'location': 'Nairobi', 'date': '21/3/2017'}])

    def test_correct_output(self):
        # Check for correct event creation
        
        msg = self.events_class_obj.createEvent(
            'TechDay', "mike@gmail.com", "Software", "Nairobi", "21/12/2017")
        self.assertEqual(
            msg, [{'owner': 'mike@gmail.com', 'name': 'TechDay', 'category': 'Software', 
                        'location': 'Nairobi', 'date': '21/12/2017'}])

    def test_editing_event(self):
        # Check for edits to event name
        
        self.events_class_obj.events_list = [{'owner': 'mike@gmail.com', 'name': 'Thanks Giving'}, {
            'owner': 'mike@gmail.com', 'name': 'Easter'}]
        msg = self.events_class_obj.editEvent(
            'Christmass', 'Thanks Giving', "mike@gmail.com")
        self.assertEqual(msg, [{'owner': 'mike@gmail.com', 'name': 'Christmass'}, {
            'owner': 'mike@gmail.com', 'name': 'Easter'}])
   

    def test_delete_event(self):
        #Check to see if event is deleted
        
        self.events_class_obj.events_list = \
        [{'owner': 'mike@gmail.com', 'name': 'TechDay'}, \
        {'owner': 'mike@gmail.com', 'name': 'Fashion'}, \
        {'owner': 'mike@gmail.com', 'name': 'FunDay'}]
        msg = self.events_class_obj.deleteEvent(
            'TechDay', "mike@gmail.com")
        self.assertEqual(msg, \
        [{'owner': 'mike@gmail.com', 'name': 'Fashion'}, \
        {'owner': 'mike@gmail.com', 'name': 'FunDay'}])


if __name__ == '__main__':
    unittest.main()
