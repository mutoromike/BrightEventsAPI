# Handle creation, deletion and editing of events
import re


class EventsClass(object):
   # Handles creation of events
    

    def __init__(self):
        # list to hold events a user creates
        self.events_list = []

    def getOwner(self, user):
        # Returns events belonging to a user
        
        user_events_list = [
            item for item in self.events_list if item['owner'] == user]
        return user_events_list

    def allEvents(self):
        # returns all existing events
        all_events = [
            item for item in self.events_list
        ]
        return all_events
    def get_event_by_name(self, event_name):
        """ return the event with the given name"""
        for event in self.events_list:
            if event['name'] == event_name:
                return event
        else:
            return False
            
    def createEvent(self, event_name, user, category, location, date):
        # Handles creation of events           
        # Check for special characters
        if re.match("^[a-zA-Z0-9 _]*$", event_name):
            # Get users shopping lists
            my_event = self.getOwner(user)
            # check if name of list already exists
            # for item in my_event:
            #     if list_name == item['name']:
            #         return "Event name already exists."
            events_dict = {
                'name': event_name,
                'owner': user,
                'category': category,
                'location': location,
                'date': date,
            }
            self.events_list.append(events_dict)
        else:
            return "No special characters (. , ! space [] )"
        return self.getOwner(user)

    def editEvent(self, edit_name, old_name, user):
        # Handles edits made to event name           
        # editted name and original name
        print(len(self.events_list))
        if re.match("^[a-zA-Z0-9 _]*$", edit_name):
            # Get users lists
            my_event = self.getOwner(user)
            events = [event for event in my_event if event["name"] == old_name]
            if not events:
                return "event Not found, Updpate failed"

            found_event = events[0]
            del found_event['name']
            edit_dict = {
                'name': edit_name
                }
            found_event.update(edit_dict) 
            return self.getOwner(user)               
        else:
            return "No special characters (. , ! space [] )"
        

    
    def deleteEvent(self, event_name, user):
        # Handles removal of events using list comprehension
        
        events = [event for event in self.events_list if event["name"] == event_name]
        if not events:
            return "Deletion failed , Event Not found"
        print(event_name)
        print("Current length of event list is ",len(self.events_list))
        found_event = events[0]
        new_event_list = [event for event in self.events_list if event["name"] != event_name]
        self.events_list = new_event_list
        print(len(self.events_list))
        print("Updated Length of event list is ",len(self.events_list))
        return self.events_list


    