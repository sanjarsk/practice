#!/usr/bin/env python3
import urllib.request as urllib2
import sys
import json
import webbrowser


user = sys.argv[1]
password = sys.argv[2]
repositories = sys.argv[3:len(sys.argv)]

# url = 'https://api.bitbucket.org/2.0/repositories/sanjarsk/min_yust_website/pullrequests?q=state+%3D+%22OPEN%22'

password_manager = urllib2.HTTPPasswordMgrWithPriorAuth()
password_manager.add_password(None, url, user, password, is_authenticated=True)
auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
opener = urllib2.build_opener(auth_manager)

data = opener.open(url).read()
data = to_dict(data)

values = data['values']
print(values)



if data['size'] >= 10:
    print('Too many pullrequests, try to filter by repo')
    sys.exit()


def open_in_browser(url):
    webbrowser.open(url, new=2, autoraise=True)


def list_repository_urls(repos):
    all_urls = []
    if repos:
        for repo in repos:
            all_urls.append('https://api.bitbucket.org/2.0/repositories/{0}/{1}/pullrequests?q=state="OPEN"'.format(user, repo))
    else:
        slugs = return_all_repo_slugs()
        for slug in slugs:
            all_urls.append('https://api.bitbucket.org/2.0/repositories/{0}/{1}/pullrequests?q=state="OPEN"'.format(user, slug))
    return all_urls




def return_all_repo_slugs():
    data = opener.open('https://api.bitbucket.org/2.0/repositories/{}'.format(user))
    data = to_dict(data)
    all_repos = []
    for i in data['values']:
        all_repos.append(i['slug'])
    return all_repos


def all_pullrequests():
    pullrequests = 
    urls = list_repository_urls(repositories)
    for url in urls:
        data = opener.open(url)
        data = to_dict(data)
        data


def to_dict(input):
    return json.loads(input.decode())


