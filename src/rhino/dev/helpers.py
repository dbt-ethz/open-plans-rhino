from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs


def AddChildLayer(lname, parent):
    # Add layer for new project
    if rs.IsLayer(lname) and rs.IsLayerParentOf(lname, parent):
        return lname
    else:
        layer = rs.AddLayer(name=lname, color=None, visible=True, locked=False, parent=parent)
        rs.ParentLayer(layer=layer, parent=parent)
        return layer

def CheckProjectExist():
    # check if project exists
    if rs.IsLayer("OpenPlans"):
        projects = rs.LayerChildren("OpenPlans")
    else:
        print("Error: Please create a project first (use OPCreateProject cmd)")
        return
    if projects:
        return True
    else:
        print("Error: Please create a project first (use OPCreateProject cmd)")
        return

