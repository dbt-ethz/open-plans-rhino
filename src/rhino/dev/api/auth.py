import urllib
import urllib2
from urllib2 import HTTPError
import json
from uri import URI


def Login(email, password):
    url = URI + '/auth/login'
    data = json.dumps({'email': email,
                       'password': password})
    req = urllib2.Request(url, data=data, headers={
                          'Content-Type': 'application/json'})

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)


def checkLoginStatus():
    url = URI + 'auth/status'
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)


def Logout():
    url = URI + 'auth/logout'
    req = urllib2.Request(url)
    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)