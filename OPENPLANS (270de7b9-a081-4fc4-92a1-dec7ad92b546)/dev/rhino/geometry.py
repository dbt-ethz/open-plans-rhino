from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from api import polygon

import rhinoscriptsyntax as rs


class Polygon:

    def __init__(self, points=None, move_y=0):
        self.__points = points
        self.__frame_h = move_y

    @property
    def points(self):
        return self.__points

    @classmethod
    def from_data(cls, data, move_y=0):
        return cls(points=[[p['x'], p['y']*-1 + move_y]
                           for p in data])

    #TODO: transform coords
    def to_data(self):
        return {"points": [{'x': p[0], 'y': p[1]} for p in self.points]}
