import urllib2
from urllib2 import HTTPError
import json
import uri


def fetch_polygon_types():
    url = uri.URI + '/polygon_type/all'
    req = urllib2.Request(url)

    try:
        response = urllib2.urlopen(req)
        json_string = response.read().decode('utf-8')
        retVal = dict(json.loads(json_string))
        return retVal
    except HTTPError as e:
        print(e)
