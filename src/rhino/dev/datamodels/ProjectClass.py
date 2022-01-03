from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import json

from datamodels.Plan import PLAN
from datamodels.Project import PROJECT
from datamodels.Polygon import POLYGON


class ProjectData:
    def __init__(self, project=PROJECT, plans=PLAN, polygons=POLYGON):
        self.__project = project
        self.__project['plans'] = plans
        self.__project['plans']['polygons'] = polygons

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
    def jsonStr(self):
        return json.dumps(self.__dict__)

    def modify_project(self, dict={}, **kwargs):
        for key in dict:
            self.__project[key] = dict[key]
        for key in kwargs:
            self.__project[key] = kwargs[key]
