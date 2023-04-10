from google.cloud import datastore
from google.auth.transport import requests
import google.oauth2.id_token
import random


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
        :return: True on success, otherwise False.
        '''
        try:
            calendar_keys = user_data['calendar_ids']
            calendar_keys.append(id)
            user_data.update({
                'calendar_ids': calendar_keys
            })
            self.datastore_client.put(user_data)
        except:
            return False
        return True

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
