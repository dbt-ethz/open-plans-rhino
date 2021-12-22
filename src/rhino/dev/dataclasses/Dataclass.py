from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class Dataclass(object):
    def __init__(self, dict, **kwargs):
        for key in dict:
            setattr(self, key, dict[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
