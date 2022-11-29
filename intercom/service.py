from .api_operations import Get, Find, All, Create

class BaseService(Get, All):
    
    def __init__(self, client, schemas=None):
        self.client = client
        self.schemas = schemas

class Admin(BaseService):
    collection = 'admins'

class Company(BaseService):
    collection = 'companies'

class Contact(BaseService, Find, Create):
    collection = 'contacts'

class Team(BaseService):
    collection = 'teams'