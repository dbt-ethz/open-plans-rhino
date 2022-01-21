from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhino.geometry as geom

import rhinoscriptsyntax as rs
import Rhino
import json


def add_parent_layer(lname, attr=None):
    if not rs.IsLayer(lname):
        lname = rs.AddLayer(name=lname, color=None,
                            visible=True, locked=False, parent=None)
        rs.CurrentLayer(lname)

    if attr:
        set_layer_user_text(layer=lname, data=attr)

    return lname


def add_child_layer(lname, parent, attr=None):
    # Add layer for new project
    if not (rs.IsLayer(lname) and rs.IsLayerParentOf(lname, parent)):
        lname = rs.AddLayer(name=lname, color=None,
                            visible=True, locked=False, parent=parent)
        rs.ParentLayer(layer=lname, parent=parent)

    ids = rs.LayerIds()
    if attr:
        set_layer_user_text(layer=ids[1], data=attr)

    return lname


def project_to_rhino_layers(project):
    """Add Project instance to Rhino document layers.

    Parameters
    ----------
    project : :class: 'OpenPlansProject'
        open plans project instance.

    Returns
    -------

    """
    # Set document user text from project
    set_document_user_text(data=project.project)

    # project layer
    project_layer = add_child_layer(
        lname=project.project_id_string, parent=add_parent_layer('OpenPlans'))

    # plan layers
    plans = project.fetch_project_plans()
    for plan in plans:
        plan_layer = add_child_layer(
            lname=plan.plan_id_string, parent=project_layer)

    # polygon layers
        polygon_layers = add_polygon_rhino_layers(plan)


def add_polygon_rhino_layers(plan):
    """Add Rhino Layers and Rhino.Polylines 
    from Plan instance Polygons.

    Parameters
    ----------
    plan : :class: 'OpenPlansPlan'
        open plans plan instance.

    Returns
    -------
    polygon_layers : list[str]
        list of layer names from polygon layers
    """
    p_layers = []
    for polygon in plan.plan_polygons():
        layer = add_child_layer(lname=' '.join(
            map(str, polygon.tags)), parent=rs.LayerName(plan.plan_id_string, fullpath=True))
        p_layers.append(layer)
        # add geometry to layer
        polyline_to_rhino_layer(
            geom=polygon.rhino_polygon(), layer=layer, attr=polygon.attributes)

    return p_layers


def polyline_to_rhino_layer(geom, layer, attr=None):
    """Add Polygon instance to Rhino document layer.

    Parameters
    ----------
    geom : :class: 'Polygon'
        Polygon instance.
    layer : str
        Rhino.Layer name
    attr : dict
        if dict, key value pairs of object's attributes
        are stored in Rhino Object User text

    Returns
    -------

    """
    obj = rs.AddPolyline(geom.points)
    rs.ObjectLayer(object_id=obj, layer=layer)

    if attr:
        set_object_user_text(object_id=obj, data=attr)


def set_document_user_text(data):
    """Set Rhino document user text.

    Parameters
    ----------
    data : dict
        data key value pairs.

    Returns
    -------

    """
    for key, value in data.iteritems():
        rs.SetDocumentUserText(key=key, value=json.dumps(value))


def get_document_user_text():
    """Returns Rhino document user text as python dictionary"""
    # remove empty spaces with split() to check for empty strings
    return {k: json.loads(rs.GetDocumentUserText(key=k)) for k in rs.GetDocumentUserText()}


def set_object_user_text(object_id, data):
    """Set Rhino Object user text.

    Parameters
    ----------
    object_id : str
        The Rhino object's identifier to which user data is assigned
    data : dict
        data key value pairs.

    Returns
    -------

    """
    for key, value in data.iteritems():
        rs.SetUserText(object_id=object_id, key=key, value=json.dumps(value))


def set_layer_user_text(layer, data):
    pass


def rhino_curve_to_data_points(obj):
    """Set Rhino document user text.

    Parameters
    ----------
    obj : str
        object_id (guid): the object's identifier.

    Returns
    -------
    points data: dict
        the points from polygon in dict format of open plans
    """
    if rs.IsCurve(obj):
        points = rs.CurvePoints(obj)
    # TODO: Flip Y coordinates to match image coordinates
    return [{'x': p.X, 'y': p.Y} for p in points]


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
