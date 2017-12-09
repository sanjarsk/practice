#!/usr/bin/env python3
import urllib.request as urllib2
import sys
import json
import webbrowser

user = sys.argv[1]
password = sys.argv[2]
in_repositories = sys.argv[3:len(sys.argv)]
url = "https://api.bitbucket.org/2.0/repositories/{}".format(user)

password_manager = urllib2.HTTPPasswordMgrWithPriorAuth()
password_manager.add_password(None, url, user, password, is_authenticated=True)
auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
opener = urllib2.build_opener(auth_manager)


def open_and_read(url):
    data = opener.open(url).read()
    return data


def to_dict(input):
    return json.loads(input.decode())


def open_in_browser(url):
    webbrowser.open(url, new=2, autoraise=True)


# compose urls for wished repos or all repos of a user
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


def all_pullrequests(in_repositories):
    total_pullrequests = []
    urls = list_repository_urls(in_repositories)
    for url in urls:
        data = open_and_read(url)
        data = to_dict(data)
        for i in data['values']:
            total_pullrequests.append(i['links']['html']['href'])
    if len(total_pullrequests) >= 10:
        print('Too many pullrequests, try to filter by repo')
        sys.exit()
    else:
        for request in total_pullrequests:
            open_in_browser(request)


def return_all_repo_slugs():
    data = open_and_read('https://api.bitbucket.org/2.0/repositories/{}'.format(user))
    data = to_dict(data)
    all_repos = []
    for i in data['values']:
        all_repos.append(i['slug'])
    return all_repos


if __name__ == "__main__":

    all_pullrequests(in_repositories)
