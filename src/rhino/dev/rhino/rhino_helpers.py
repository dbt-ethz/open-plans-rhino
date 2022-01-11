from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs


def add_parent_layer(lname):
    if rs.IsLayer(lname):
        return lname
    else:
        parent = rs.AddLayer(name=lname, color=None,
                             visible=True, locked=False, parent=None)
        rs.CurrentLayer(parent)
        return parent


def add_child_layer(lname, parent):
    # Add layer for new project
    if rs.IsLayer(lname) and rs.IsLayerParentOf(lname, parent):
        return lname
    else:
        layer = rs.AddLayer(name=lname, color=None,
                            visible=True, locked=False, parent=parent)
        rs.ParentLayer(layer=layer, parent=parent)
        return layer


def project_to_rhino_layers(project_cls):
    init = add_parent_layer('OpenPlans')
    project_layer = add_child_layer(
        lname=project_cls.project_id_string(), parent=init)
    for id in project_cls.plan_ids:
        pass


def op_project_exists(func):

    def wrapper(*args):
        # check if project exists
        if rs.IsLayer("OpenPlans"):
            projects = rs.LayerChildren("OpenPlans")
            print(projects)
            if projects:
                func()
            else:
                print("Error: Please create a project first (use OPCreateProject cmd)")
        else:
            print("Error: Please create a project first (use OPCreateProject cmd)")

    return wrapper
