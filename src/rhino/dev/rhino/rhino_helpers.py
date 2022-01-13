from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhino.geometry as geom

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


def project_to_rhino_layers(project):
    project_layer = add_child_layer(
        lname=project.project_id_string, parent=add_parent_layer('OpenPlans'))

    plans = project.fetch_project_plans()
    for plan in plans:
        plan_layer = plan_to_rhino_layer(
            plan, project_layer=project_layer)

        # add polygons
        polygons_layers = [polygon_to_rhino_layer(polygon=polygon)
                           for polygon in plan.plan_polygons()]


def plan_to_rhino_layer(plan, project_layer):
    return add_child_layer(lname=plan.plan_id_string, parent=project_layer)


def polygon_to_rhino_layer(polygon):
    geom = polygon.rhino_polygon()
    polygon_layer = add_child_layer(lname=' '.join(
        map(str, polygon.tags)), parent="00 Level; ID: 963")
    rs.ObjectLayer(object_id=rs.AddPolyline(geom.points), layer=polygon_layer)


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
