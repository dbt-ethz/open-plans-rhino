from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhino.geometry_objs as geom
import api

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


def project_id_string(project_dict):
    return "ID: {}; Name: {}".format(project_dict['id'],
                                     project_dict['name'])


def project_to_rhino_layers(project):
    init = add_parent_layer('OpenPlans')
    project_layer = add_child_layer(
        lname=project_id_string(project), parent=init)
    for p in project['plans']:
        plan = api.get_data(dict=api.fetch_plan(plan_id=p['id']), key='plan')
        floor_layer = add_child_layer(lname=str(plan['floor']).zfill(
            2) + '_floor', parent=project_layer)

        for d in plan['polygons']:
            p = geom.Polygon(data=d)
            polygon_layer = add_child_layer(lname=p.tags[0], parent=floor_layer)
            rs.ObjectLayer(rs.AddPolyline(p.points), layer=polygon_layer)


def op_project_exists(func):

    def wrapper(*args):
        # check if project exists
        if rs.IsLayer("OpenPlans"):
            projects = rs.LayerChildren("OpenPlans")
            if projects:
                func()
            else:
                print("Error: Please create a project first (use OPCreateProject cmd)")
        else:
            print("Error: Please create a project first (use OPCreateProject cmd)")

    return wrapper
