import json
import http.client

#constants for api calls
headers = {'User-Agent': 'jongodshall'}    #this goes in config in the real world, but I can just be me for this purpose
conn = http.client.HTTPSConnection('api.github.com')

def get_json_content(path):
    conn.request('GET', path, headers=headers)

    response = conn.getresponse()
    if not response.status == 200:
        raise ValueError('Unable to connect to %s' % path)

    return response.read().decode()

#classes to represent a pull request and associated objects.  This is a best guess at what fields we are interest in; the questions for part 2 will shape this
class PullRequest:
    def __init__(self, id):
        self.id = id

class User:
    def __init__(self, id, username, is_site_admin):
        self.id = id
        self.name = username
        self.is_admin = is_site_admin

class Repo:
    def __init__(self, id, name, org):
        self.id = id
        self.name = name
        self.org = org

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'

    def get_pull_requests(self):
        json_string = get_json_content('/repos/%s/%s/pulls' % (self.org, self.name))

        #Miniimum dataset should be who requested it, when was it requested, has it been merged and by who
        return []


#get the list of repos for the organization
def get_org_repos(org):
    json_string = get_json_content('/orgs/%s/repos' % org)
    response_repos = json.loads(json_string)


    return [Repo(obj['id'], obj['name'], org) for obj in response_repos]


#main block
def main():
    repos = get_org_repos('lodash')

    for repo in repos:
        print(repo.name + ' - ' + str(repo.get_pull_requests()))


if __name__ == "__main__": main()
