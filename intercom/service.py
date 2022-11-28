from .api_operations import Get, Find, All

class BaseService(Get):
    
    def __init__(self, client):
        self.client = client

class Admin(BaseService, All):
    collection = 'admins'

class Company(BaseService, All):
    collection = 'companies'

class Contact(BaseService, Find, All):
    collection = 'contacts'