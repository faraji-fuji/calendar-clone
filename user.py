from google.cloud import datastore
from google.auth.transport import requests
import google.oauth2.id_token
from pprint import pprint


class User:
    def __init__(self):
        self.datastore_client = datastore.Client()
        self.firebase_request_adapter = requests.Request()

    def create_user(self, claims):
        '''
        Create user data from claims object.

        :param claims: An object returned after firebase token verification
        :return: On success, True, otherwise False.
        '''
        try:
            entity_key = self.datastore_client.key('User', claims['email'])
            entity = datastore.Entity(key=entity_key)
            entity.update({
                'email': claims['email'],
                'name': claims['name'],
                'calendar_ids': [],
                'shared_calendar_ids': []
            })
            self.datastore_client.put(entity)
        except:
            return False
        return True

    def get_user(self, claims):
        '''
        Get a user entity from the data store

        :param claims: An object returned after firebase token verification.
        :return: A user entity containing user data of the logged in user.
        '''
        entity_key = self.datastore_client.key('User', claims['email'])
        entity = self.datastore_client.get(entity_key)
        return entity
