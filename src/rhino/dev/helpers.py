from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs


def AddParentLayer(lname):
    if rs.IsLayer(lname):
        return lname
    else:
        parent = rs.AddLayer(name=lname, color=None,
                             visible=True, locked=False, parent=None)
        rs.CurrentLayer(parent)
        return parent


def AddChildLayer(lname, parent):
    # Add layer for new project
    if rs.IsLayer(lname) and rs.IsLayerParentOf(lname, parent):
        return lname
    else:
        layer = rs.AddLayer(name=lname, color=None,
                            visible=True, locked=False, parent=parent)
        rs.ParentLayer(layer=layer, parent=parent)
        return layer


def merge_dicts(dict_a, dict_b):
    c = dict_a.copy()
    c.update(dict_b)
    return c
