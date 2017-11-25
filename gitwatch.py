import sys
import json
import http.client
from datetime import datetime
from urllib.parse import urlparse, parse_qs

#constants for api calls
headers_raw = open('token.txt', 'r').read()
headers = json.loads(headers_raw)
conn = http.client.HTTPSConnection('api.github.com')

def get_json_content(path):
    conn.request('GET', path, headers=headers)
    next_page = None
    response = conn.getresponse()
    if not response.status == 200:
        raise ValueError('Unable to connect to %s' % path)

    link = response.getheader('Link')
    if link:
        for l in link.split(','):
            elmts = l.split(';')
            if elmts[1] == ' rel="next"':
                parsed_url = urlparse(elmts[0].replace('>',""))
                qs = parse_qs(parsed_url.query)
                if 'page' in qs:
                    next_page = qs['page'][0]

    return (response.read().decode(), next_page)

#classes to represent a pull request and associated objects.  This is a best guess at what fields we are interest in; the questions for part 2 will shape this
class PullRequest:
    def __init__(self, id):
        self.id = id

    def __str__(self):
        merge_text = 'Merged' if self.merged else 'Not Merged'
        return '%s - %s at %s (%s)\n' % (str(self.id), self.user.name, str(self.created_at), merge_text)

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

    def clear_pull_requests(self):
        self.pull_requests = []

    def refresh_pull_requests(self, page=1, load_details=False):
        #print('Fetching /repos/%s/%s/pulls?state=all' % (self.owner, self.name))
        json_string, next_page = get_json_content('/repos/%s/%s/pulls?state=all&per_page=100&page=%s' % (self.owner, self.name, page))

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

            #This is likely to be useful info, but it chews up a lot of requests and they are rate limited.  Use only if needed
            if load_details and pull_request.merged:
                merge_details = get_json_content('/repos/%s/%s/pulls/%s' % (self.owner, self.name, obj['number']))
                try:
                    pull = json.loads(merge_details)
                    pull_request.merged_at = datetime.strptime(pull['merged_at'],'%Y-%m-%dT%H:%M:%SZ')
                    pull_request.merged_by = User(pull['merged_by']['id'], pull['merged_by']['login'], pull['merged_by']['site_admin'])
                except:
                    print('Could not load merge details: /repos/%s/%s/pulls/%s' % (self.owner, self.name, obj['number']))

            self.pull_requests.append(pull_request)

        #ret = sorted(ret, key=lambda p: p.created_at)    #Wait and see if a primary sort makes sense.  Also, turns out this is the default sort anyway
        #unclear if this is better served as a property or a return... depends on whether the main use cases care about organizing by repo

        if (next_page):
            self.refresh_pull_requests(next_page)


#get the list of repos for the organization
def get_org_repos(org):
    json_string, next_page = get_json_content('/orgs/%s/repos' % org)

    try:
        response_repos = json.loads(json_string)
    except:
        print('Unable to parse json string: %s' % json_string)

    return [Repo(obj['id'], obj['name'], org) for obj in response_repos]

#main block
def main():
    try:
        org = sys.argv[1]
    except:
        print('Please provide an org name.')
        return

    repos = get_org_repos(org)

    for repo in repos:
        f = open('tmp/%s.txt' % repo.name, 'w')
        repo.refresh_pull_requests()
        print('%s - %d' % (repo.name, len(repo.pull_requests)))
        for p in repo.pull_requests:
            f.write(str(p))

    conn.close()


if __name__ == "__main__": main()
