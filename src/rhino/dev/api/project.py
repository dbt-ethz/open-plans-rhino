import urllib2
from urllib2 import HTTPError
import json
from uri import URI


def save_project(project):
    url = URI + '/project/save'
    data = json.dumps(project)
    req = urllib2.Request(url)
    req.add_data(data)

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)


def fetch_project(project_id):
    url = URI + '/project/fetch/{}'.format(project_id)
    req = urllib2.Request(url)

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)


def fetch_account_project(account_id, number, page=1):
    url = URI + \
        '/project/fetch/account/{}?number={}&page={}'.format(
            account_id, number, page)
    req = urllib2.Request(url)

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)
