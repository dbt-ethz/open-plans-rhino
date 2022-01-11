from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs


class Polygon:

    def __init__(self, data):
        self.points = [self.transform_to_rhino_coord(x=p['x'], y=p['y'])
                       for p in data['points']]
        self.tags = data['tags']

    @staticmethod
    def transform_to_rhino_coord(x, y):
        """ 
        Flip y coordinate to match Rhino system
        Starting top left as 0, 0

        Returns : [ x, y ] 
        """
        return list([x, y*-1])

    @staticmethod
    def to_data(x_coords, y_coords):
        coords = [{'x': x, 'y': y} for x, y in zip(x_coords, y_coords)]
        return {'points': coords}
