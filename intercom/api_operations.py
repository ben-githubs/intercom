from datetime import datetime
import json
import time

from schema import Schema

def deep_exists(obj, path):
    fields = path.split('.')
    for field in fields:
        if field in obj:
            obj = obj[field]
        else:
            return False
    return True

def deep_get(obj, path, default=None):
    fields = path.split('.')
    if not deep_exists(obj, path):
        return default
    for field in fields:
        obj = obj[field]
    return obj

class Get:
    def get(self, id):
        return self.client.get(f"{self.collection}/{id}")

class Find(object):
    def find(self, **kwargs):
        query = list()
        for field, value in kwargs.items():
            query.append({
                'field': field,
                'operator': '=',
                'value': value
            })
        if len(query) > 1:
            query = {
                'operator': 'AND',
                'value': query
            }
        else:
            query = {'query': query[0]}
        print(query)
        return self.client.post(f"{self.collection}/search", body=query)

class All:
    def all(self):
        endpoint = self.collection
        return self.client.get(endpoint)


class Create:
    def new(self, **kwargs):
        # Validate input arguments
        self.schemas.new.validate(kwargs)

        # Convert to JSON
        data = json.dumps(kwargs, default=object_hook)

        return self.client.post(self.collection, body=data)

class Delete:
    def delete(self, id: str):
        id = str(id)
        endpoint = self.collection + '/' + id
        return self.client.delete(endpoint)

def object_hook(data):
    if isinstance(data, datetime):
        return time.mktime(data.timetuple())
    return data