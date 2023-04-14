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
        entity_key = self.datastore_client.key('UserData', claims['email'])
        entity = datastore.Entity(key=entity_key)
        entity.update({
            'email': claims['email'],
            # 'name': claims['name'],
            'calendar_ids': [],
            'share_requests': [],
            'shared_calendar_ids': []
        })
        self.datastore_client.put(entity)

    def update_username(self, claims):
            '''
            Workaround to update username. Firebase seems not to return the 
            name on first verification. We'll need to update manually. 

            :param claims: An object returned after firebase token verification
            '''
            entity_key = self.datastore_client.key('UserData', claims['email'])
            entity = datastore.Entity(key=entity_key)
            entity.update({
                'name': claims['name']
            })
            self.datastore_client.put(entity)

    def get_user(self, claims):
        '''
        Get a user entity from the data store

        :param claims: An object returned after firebase token verification.
        :return: A user entity containing user data of the logged in user.
        '''
        entity_key = self.datastore_client.key('UserData', claims['email'])
        entity = self.datastore_client.get(entity_key)
        return entity


    def get_user_entity(self, email):
        '''
        Get a user entity with the corresponding email address

        :param email: Email address of the user.
        :return: A user entity containing user data of the associated email.
        '''
        entity_key = self.datastore_client.key('UserData', email)
        entity = self.datastore_client.get(entity_key)
        return entity

    def get_share_requests(self, user_data):
        '''
        Get share requests from other users.

        :param user_data: User data.
        :return: Share requests.
        '''
        share_requests = []
        user_entity_key = self.datastore_client.key('UserData', user_data['email'])
        user_entity = self.datastore_client.get(user_entity_key)
        share_requests = user_entity['share_requests']
        return share_requests