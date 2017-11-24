import json
import http.client

class Repo:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'


#first
headers = {'User-Agent': 'jongodshall'}
conn = http.client.HTTPSConnection('api.github.com')
conn.request('GET', '/orgs/Lodash/repos', headers=headers)

response = conn.getresponse()
json_string = response.read().decode()
response_repos = json.loads(json_string)

repos = [Repo(obj['id'], obj['name']) for obj in response_repos]

print(repos)
