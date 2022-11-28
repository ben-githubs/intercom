from .api_operations import Get, Find, All

class BaseService(Get, All):
    
    def __init__(self, client):
        self.client = client

class Admin(BaseService):
    collection = 'admins'

class Company(BaseService):
    collection = 'companies'

class Contact(BaseService, Find):
    collection = 'contacts'

class Team(BaseService):
    collection = 'teams'