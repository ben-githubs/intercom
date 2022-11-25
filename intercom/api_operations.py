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
        results = list()
        endpoint = self.collection
        while endpoint:
            endpoint = endpoint.replace(self.client.host, '')
            resp = self.client.get(endpoint)
            results += resp
            endpoint = deep_get(resp, 'pages.next')
        return results

class AllCursor:
    def all(self):
        results = list()
        starting_after = ''
        first_run = True
        i = 0
        while starting_after or first_run:
            first_run = False
            if starting_after:
                resp = self.client.get(self.collection, starting_after = starting_after)
            else:
                resp = self.client.get(self.collection)
            results += resp
            starting_after = deep_get(resp, 'pages.next.starting_after')
        return results
