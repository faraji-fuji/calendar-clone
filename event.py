from google.cloud import datastore
from google.auth.transport import requests
import google.oauth2.id_token
import random


class Event:
    def __init__(self):
        self.datastore_client = datastore.Client()
        self.firebase_request_adapter = requests.Request()

    def create_event(self, name, start_time, end_time, notes):
        '''
        Create an event entity.

        :param name: The name of the event.
        :param start_time: Start time of the event.
        :param end_time: The end time of the event.
        :param notes: Notes about the event.
        :return: True on success, otherwise False.
        '''
        try:
            id = random.getrandbits(63)
            entity_key = self.datastore_client.key('Event', id)
            entity = datastore.Entity(key=entity_key)
            entity.update({
                'name': name,
                'start_time': start_time,
                'end_time': end_time,
                'notes': notes
            })
            self.datastore_client.put(entity)
        except:
            return False
        return id

    def add_event_to_calendar(self, calendar, id):
        '''
        Attach the ID of an event to a calendar

        :param calendar: Calendar entity to add the event to.
        :param id: The ID of the event.
        :return: True on success, otherwise False.
        '''
        try:
            event_ids = calendar['event_ids']
            event_ids.append(id)
            calendar.update({
                'event_ids': event_ids
            })
            self.datastore_client.put(event_ids)
        except:
            return False
        return True
