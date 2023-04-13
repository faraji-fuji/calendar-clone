from google.cloud import datastore
from google.auth.transport import requests
import random
from pprint import pprint

class MyCalendar:
    def __init__(self):
        self.datastore_client = datastore.Client()
        self.firebase_request_adapter = requests.Request()

    def create_calendar(self, name):
        '''
        Create a calendar entity.

        :param name: The name of the calendar.
        :return: ID of the calendar entity.
        '''
        id = random.getrandbits(63)
        entity_key = self.datastore_client.key('Calendar', id)
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'name': name,
            'event_ids': [],
        })
        self.datastore_client.put(entity)
        return id

    def add_calendar_to_user(self, user_data, id):
        '''
        Add the ID of a calendar entity to a list of containing calendar IDs.
        The List is a property of User.

        :param user_data: A User entity. Where we need to add the ID.
        :param id: The ID of the new calendar.
        '''
        calendar_keys = user_data['calendar_ids']
        calendar_keys.append(id)
        user_data.update({
            'calendar_ids': calendar_keys
        })
        self.datastore_client.put(user_data)

    def get_calendars_from_user(self, user_data):
        '''
        Get a list of  calendars of the current user. 

        :param user_data: An entity of kind User.
        :return: A list of entities of kind Calendar, that belong to the User.
        '''
        calendar_ids = user_data['calendar_ids']
        calendar_keys = []
        for i in range(len(calendar_ids)):
            calendar_keys.append(self.datastore_client.key(
                'Calendar', calendar_ids[i]))

        calendar_list = self.datastore_client.get_multi(calendar_keys)
        return calendar_list

    def get_calendar_entity():
        pass

    def get_shared_calendars(self, user_data):
        '''
        Get a list of shared calendars.

        :param user_data: A entity of Kind User. Contains data about the user.
        :return: A list of shared calendars. 
        '''
        shared_calendar_ids = user_data['shared_calendar_ids']
        shared_calendar_keys = []
        for i in range(len(shared_calendar_ids)):
            shared_calendar_keys.append(self.datastore_client.key(
                'Calendar', shared_calendar_ids[i]))

        shared_calendar_list = self.datastore_client.get_multi(
            shared_calendar_keys)
        return shared_calendar_list
    
    def update_calendar(self, calendar, id):
        '''
        Update a calendar entity.

        :param calendar: The calendar entity to update.
        :param id: The ID of the event to be added to the event list
        '''
        event_ids = calendar['event_ids']
        event_ids.append(id)
        calendar.update({
            'event_ids': event_ids
        })
        self.datastore_client.put(calendar)


    def update_calendar_name(self, calendar, new_name):
        '''
        Update the name of a calendar

        :param calendar: The calendar entity to update.
        :param new_name: New name of the calendar.
        '''
        calendar.update({
            'name': new_name
        })
        self.datastore_client.put(calendar)


        # calendar_key = self.datastore_client.key('Calendar', calendar_id)
        # calendar_entity = self.datastore_client.get(calendar_key)

        # if calendar_entity is not None:
        #     calendar_entity.update({
        #         'name': new_name
        #     })
        #     self.datastore_client.put(calendar_entity)



    def delete_event_id(self, calendar_entity, event_id):
        '''
        Delete event id from calendar['event_ids'] list.
 
        :param calendar_ntity: The calendar entity to delete from.
        :param event_id: The ID of the event to be removed to the event list
        '''
        event_ids = calendar_entity['event_ids']
        event_ids.remove(event_id)
        calendar_entity.update({
            'event_ids': event_ids
        })
        self.datastore_client.put(calendar_entity)

        
