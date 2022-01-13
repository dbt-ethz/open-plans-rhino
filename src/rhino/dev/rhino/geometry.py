from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from api import polygon

import rhinoscriptsyntax as rs


class Polygon:

    def __init__(self, points=None):
        self.__points = points

    @property
    def points(self):
        return self.__points

    @classmethod
    def from_data(cls, data):
        return cls(points=[[p['x'], p['y']*-1]
                           for p in data])

    def to_data(self):
        return {"points": [{'x': p[0], 'y': p[1]} for p in self.points]}

