import json
import typing

import requests

from .api_resource import object_hook

class Client:
    host = 'https://api.intercom.io'

    def __init__(self, token: str = None):
        self.token = token
        pass

    @property
    def admins(self):
        from .service import Admin
        return Admin(self)
    
    @property
    def companies(self):
        from .service import Company
        return Company(self)
    
    @property
    def contacts(self):
        from .service import Contact 
        from .api_schemas import Contact as schema
        return Contact(self, schema)
    
    @property
    def teams(self):
        from .service import Team
        return Team(self)

    def get(self, endpoint, **kwargs):
        """ PUT Request: **kwargs are passed as URL parameters.
        """
        r = requests.get(f"{Client.host}/{endpoint}", params=kwargs, headers=self.__headers)
        return self.__parse_resp(r)
    
    def post(self, endpoint, body):
        """ POST Request: body is the data to send in the request body.
        """
        r = requests.post(f"{Client.host}/{endpoint}", data=body, headers=self.__headers)
        return self.__parse_resp(r)
    
    def delete(self, endpoint):
        """ DELETE Request
        """
        r = requests.delete(f"{Client.host}/{endpoint}")
        return self.__parse_resp(r)
    
    def put(self, endpoint, body):
        """ PUT Request: body is the data to send in the request body.
        """
        r = requests.put(f"{Client.host}/{endpoint}", data=json.dumps(body), headers=self.__headers)
        return self.__parse_resp(r)
    
    def __parse_resp(self, resp):
        """ Performs processing on the results of all api requests.
        """
        has_error = False
        try:
            resp.raise_for_status()
        except:
            has_error = True
            print(resp.json())
        if has_error:
            resp.raise_for_status()

        return resp.json(object_hook = lambda x: object_hook(x, self))
    
    @property
    def __headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

class Contact:
    collection_name = 'contacts'