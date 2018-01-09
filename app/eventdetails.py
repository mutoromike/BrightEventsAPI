"""eventdetails.py"""
import re
from app.events import EventsClass


class EventDetails(object):
    """ Handles details of events """
    

    def __init__(self):
        """ A list to add RSVP to events """
        self.rsvp_list = []
        

    def ownerEvents(self, user, event_name):
        """ Returns event details """
        
        user_events = [item for item in self.rsvp_list if item['owner']
                      == user and item['event'] == event_name]
        return user_events

    def events(self, event_name):
        """ returns all existing events """
        all_events = [
            item for item in events_obj.events_list
        ]
        return all_events

    def addGuest(self, event_name, user, email):
        """ Handles adding new guest to an event """

        activity_dict = {}

        temp_guets = [guest for guest in self.rsvp_list if guest["guest"] == user]
        if not temp_guets:
            activity_dict['event'] = event_name
            activity_dict['guest'] = user
            activity_dict['mail'] = email
            self.rsvp_list.append(activity_dict)
            print(activity_dict)
            return "Successful RSVP"
        
        return "You have already RSVP to this event"

    def viewGuests(self, event_name):
        """ Return guests who RSVP to an event """
        guests = [item['mail'] for item in self.rsvp_list if item['event'] == event_name]
        return guests
 
                        

    
