import json
import http.client
from datetime import datetime

#constants for api calls
headers_raw = open('token.txt', 'r').read()
headers = json.loads(headers_raw)
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

    def __str__(self):
        merge_text = 'Merged' if self.merged else 'Not Merged'
        return self.user.name + " at " + str(self.created_at) + ' (%s)' % merge_text

class User:
    def __init__(self, id, username, is_site_admin):
        self.id = id
        self.name = username
        self.is_admin = is_site_admin

class Repo:
    def __init__(self, id, name, owner, **kwargs):
        self.id = id
        self.name = name
        self.owner = owner
        self.pull_requests = []
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return self.name + ' (' + str(self.id) + ')'

    def refresh_pull_requests(self, load_details=False):
        ret = []
        print('Fetching /repos/%s/%s/pulls?state=all' % (self.owner, self.name))
        json_string = get_json_content('/repos/%s/%s/pulls?state=all' % (self.owner, self.name))

        try:
            pulls = json.loads(json_string)
        except:
            print('Unable to parse json string: %s' % json_string)

        #Miniimum dataset should be who requested it, location of the new repo, when was it requested, has it been merged and by who
        for obj in pulls:
            pull_request = PullRequest(obj['id'])
            pull_request.created_at = datetime.strptime(obj['created_at'],'%Y-%m-%dT%H:%M:%SZ')

            pull_request.user = User(obj['user']['id'], obj['user']['login'], obj['user']['site_admin'])
            pull_request.merged = False if obj['merged_at'] == None else True

            #This is likely to be userful info, but it chews up a lot of requests and they are rate limited.  Use only if needed
            if load_details and pull_request.merged:
                merge_details = get_json_content('/repos/%s/%s/pulls/%s' % (self.owner, self.name, obj['number']))
                try:
                    pull = json.loads(merge_details)
                    pull_request.merged_at = datetime.strptime(pull['merged_at'],'%Y-%m-%dT%H:%M:%SZ')
                    pull_request.merged_by = User(pull['merged_by']['id'], pull['merged_by']['login'], pull['merged_by']['site_admin'])
                except:
                    print('Could not load merge details: /repos/%s/%s/pulls/%s' % (self.owner, self.name, obj['number']))

            ret.append(pull_request)

        #ret = sorted(ret, key=lambda p: p.created_at)    #Wait and see if a primary sort makes sense
        #unclear if this is better served as a property or a return... depends on whether the main use cases care about organizing by repo
        self.pull_requests = ret


#get the list of repos for the organization
def get_org_repos(org):
    json_string = get_json_content('/orgs/%s/repos' % org)

    try:
        response_repos = json.loads(json_string)
    except:
        print('Unable to parse json string: %s' % json_string)

    return [Repo(obj['id'], obj['name'], org) for obj in response_repos]


#main block
def main():
    repos = get_org_repos('lodash')

    for repo in repos:
        repo.refresh_pull_requests()
        print(repo.name)
        for p in repo.pull_requests:
            print('\t' + str(p))

    conn.close()

if __name__ == "__main__": main()
