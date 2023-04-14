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
        calendar_ids = user_data['calendar_ids']
        calendar_ids.append(id)
        entity_key = self.datastore_client.key('UserData', user_data['email'])
        entity = self.datastore_client.get(entity_key)
        entity.update({
            'calendar_ids': calendar_ids
        })
        self.datastore_client.put(entity)

    def calendar_share_request(self, user_data, id):
        '''
        Add the ID of a calendar entity to a list containing calendar IDs that
        users have requested to share. The List is a property of User.

        :param user_data: A User entity. Where we need to add the ID.
        :param id: The ID of the calendar to be shared.
        '''
        share_requests = user_data['share_requests']

        pprint(id)
        pprint(share_requests)

        share_requests.append(id)
        pprint(share_requests)

        entity_key = self.datastore_client.key('UserData', user_data['email'])
        entity = self.datastore_client.get(entity_key)
        entity.update({
            'share_requests': share_requests
        })
        self.datastore_client.put(entity)

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


    def delete_event_id(self, calendar_entity, event_id):
        '''
        Delete event id from calendar['event_ids'] list.
 
        :param calendar_entity: The calendar entity to delete from.
        :param event_id: The ID of the event to be removed to the event list
        '''
        event_ids = calendar_entity['event_ids']
        event_ids.remove(event_id)
        calendar_entity.update({
            'event_ids': event_ids
        })
        self.datastore_client.put(calendar_entity)


    def delete_calendar(self, calendar):
        '''
        Delete a calendar entity.
        '''
        self.datastore_client.delete(calendar)


    def delete_calendar_id(self, calendar, user_data):
        '''
        Delete calendar id from UserData entity.

        :param calendar: The calendar whose ID should be deleted
        :user_data: User data.
        '''
        calendar_ids = user_data['calendar_ids']
        calendar_id = calendar.id
        calendar_ids.remove(calendar_id)
        user_entity_key = self.datastore_client.key('UserData', user_data['email'])
        user_entity = self.datastore_client.get(user_entity_key)
        user_entity.update({
            'calendar_ids': calendar_ids
        })
        self.datastore_client.put(user_entity)
        
    def check_name_exists(self, calendar_name, calendar_names):
        '''
        Check if a calendar name already exists

        :parama:
        '''
        if calendar_name in calendar_names:
            return True
        return False

    def get_calendar_names(self, user_data):
        '''
        Get a list of calendar names.

        :param user_data: User data.
        :return: A list of existing calendar names.
        '''
        calendar_names = []
        calendar_keys = []
        calendar_ids = user_data['calendar_ids']
        
        for i in range(len(calendar_ids)):
            calendar_keys.append(self.datastore_client.key(
                'Calendar', calendar_ids[i]))

        calendar_list = self.datastore_client.get_multi(calendar_keys)

        for calendar in calendar_list:
            calendar_names.append(calendar['name'])

        return calendar_names
    
    def get_calendar(self, calendar_id):
        '''
        Get calendar from datastore.

        :param calendar_id: The calendar id to get.
        :return: calendar entity. 
        '''
        calendar_entity_key = self.datastore_client.key('Calendar', calendar_id)
        calendar_entity = self.datastore_client.get(calendar_entity_key)
        return calendar_entity

    
        


        
