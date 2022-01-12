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


def plan_id_string(plan_dict):
    return "{} Level; ID: {}".format(str(plan_dict['floor']).zfill(2), plan_dict['id'])


def project_to_rhino_layers(project):
    project_layer = add_child_layer(
        lname=project.project_id_string, parent=add_parent_layer('OpenPlans'))

    plans = project.fetch_project_plans()
    for plan in plans:
        plan_layer = plan_to_rhino_layer(
            plan, project_layer=project_layer)

        # polygons = [geom.Polygon.from_data(data=data) for data in plan['polygons']]
        # for p in polygons:
        #     polygon_to_rhino_layer(p)

        # for item_p in item_f['polygons']:
        #     polygon = geom.Polygon.from_data(data=item_p)
        # p = geom.Polygon.from_data(data=d)
        # polygon_layer = add_child_layer(lname=p.tags[0], parent=floor_layer)
        # rs.ObjectLayer(rs.AddPolyline(p.points), layer=polygon_layer)


def plan_to_rhino_layer(plan, project_layer):
    return add_child_layer(lname=plan.plan_id_string, parent=project_layer)


def polygon_to_rhino_layer(polygon):
    pass
    #rs.ObjectLayer(object_id=rs.AddPolyline(polygon.points), layer='test')


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
