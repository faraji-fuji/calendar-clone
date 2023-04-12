from google.cloud import datastore
from google.auth.transport import requests
import google.oauth2.id_token
import random
from pprint import pprint


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
        :return: ID of the created event.
        '''
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
        return id
    
    def get_event_entity(self, event_id):
        '''
        Get event entity.

        :param event_id: The event ID of the event entity.s
        :return: Event entity
        '''
        event_key = self.datastore_client.key('Event', event_id)
        event_entity = self.datastore_client.get(event_key)
        return event_entity
    
    def update_event_entity(self, event_id, name, start_time, end_time, notes):
        '''
        Update an event entity

        :param event_id: The event of the entity to update. 
        '''
        event_key = self.datastore_client.key('Event', event_id)
        event_entity = self.datastore_client.get(event_key)
        event_entity.update({
            'name': name,
            'start_time': start_time,
            'end_time': end_time,
            'notes': notes
        })
        self.datastore_client.put(event_entity)

        


    def add_event_to_calendar(self, calendar, id):
        '''
        Attach the ID of an event to a calendar

        :param calendar: Calendar entity to add the event to.
        :param id: The ID of the event.
        '''

        event_ids = calendar['event_ids']
        event_ids.append(id)
        calendar.update({
            'event_ids': event_ids
        })
        self.datastore_client.put(event_ids)

    def get_personal_events(self, event_ids):
        '''
        Get a list of events from the personal calendar.

        :param event_ids: A list of event ids from the personal calendar.
        :return: A list of events from the personal calendar. 
        '''
        event_keys=[]
        for i in range(len(event_ids)):
            event_keys.append(self.datastore_client.key('Event', event_ids[i]))
        events_list = self.datastore_client.get_multi(event_keys)
        return events_list


    


    def delete_event(self, event_id):
        '''
        Delete an event entity.
        '''
        # delete entity
        event_key = self.datastore_client.key('Event', event_id)
        self.datastore_client.delete(event_key)



