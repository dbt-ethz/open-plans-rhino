import urllib2
from urllib2 import HTTPError
import json
import cookielib

import uri


def save_project(project):
    url = uri.URI + 'project/save'
    data = json.dumps(project)
    req = urllib2.Request(url, data=data, headers={
                          'Content-Type': 'application/json'})

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)
        raise


def fetch_project(project_id):
    url = uri.URI + 'project/fetch/{}'.format(project_id)
    req = urllib2.Request(url)

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)


def fetch_account_project(account_id, number, page=1):
    url = uri.URI + \
        'project/fetch/account/{}?number={}&page={}'.format(
            account_id, number, page)
    req = urllib2.Request(url)

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)
