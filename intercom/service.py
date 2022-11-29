from .api_operations import All, Create, Delete, Get, Find

class BaseService(Get, All):
    
    def __init__(self, client, schemas=None):
        self.client = client
        self.schemas = schemas

class Admin(BaseService):
    collection = 'admins'

class Company(BaseService):
    collection = 'companies'

class Contact(BaseService, Find, Create, Delete):
    collection = 'contacts'

class Team(BaseService):
    collection = 'teams'