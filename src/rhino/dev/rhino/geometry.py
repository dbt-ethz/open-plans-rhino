from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from api import polygon

import rhinoscriptsyntax as rs


class Polygon:

    def __init__(self, id=None, plan_id=None, tags=None, points=None):
        self.__id = id
        self.__plan_id = plan_id
        self.__tags = tags
        self.__points = points

    @property
    def id(self):
        return self.__id

    @property
    def plan_id(self):
        return self.__plan_id

    @property
    def tags(self):
        return self.__tags

    @property
    def points(self):
        return self.__points

    @classmethod
    def from_data(cls, data):
        return cls(id=data['id'],
                   plan_id=data['plan_id'],
                   tags=data['tags'],
                   points=[[p['x'], p['y']*-1]
                           for p in data['points']])

    def to_data(self):
        return {"id": self.id,
                "plan_id": self.plan_id,
                "points": [{'x': p[0], 'y': p[1]} for p in self.points],
                "tags": self.tags}

    def add_tag(self):
        pass

