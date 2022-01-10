from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import json

from datamodels.plan_model import PLAN
from datamodels.project_model import PROJECT
from datamodels.polygon_model import POLYGON
import api


class ProjectData:
    def __init__(self, project=PROJECT, plans=PLAN, polygons=POLYGON):
        self.__project = project
        self.__project['plans'].extend(plans)

    @property
    def project(self):
        return self.__project

    @property
    def plans(self):
        return self.__project['plans']

    @property
    def polygons(self):
        return self.__project['plans']['polygons']

    @property
    def name(self):
        return self.project['name']

    @property
    def jsonStr(self):
        return json.dumps(self.__dict__)

    def modify_project(self, dict={}, **kwargs):
        for key in dict:
            self.__project[key] = dict[key]
        for key in kwargs:
            self.__project[key] = kwargs[key]
        return self

    def save_project_to_openplans(self):
        resp = api.save_project(self.project)
        if resp['succeeded']:
            project_id = resp['project_id']
            return project_id
        else:
            print(resp['error'])

    def __repr__(self):
        return "{}(project={})".format(self.__class__.__name__, self.project)
