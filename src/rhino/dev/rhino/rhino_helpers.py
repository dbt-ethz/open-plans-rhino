from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import datamodels

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
import json


def add_parent_layer(lname, attr=None):
    if not rs.IsLayer(lname):
        lname = rs.AddLayer(name=lname, color=None,
                            visible=True, locked=False, parent=None)
        rs.CurrentLayer(lname)

    layer_id = rs.LayerId(lname)

    if attr:
        set_layer_user_text(layer=lname, data=attr)

    return lname, layer_id


def add_child_layer(lname, parent, attr=None):
    # Add layer if it does not exist yet
    if not (rs.IsLayer(lname) and rs.IsLayerParentOf(lname, parent)):
        lname = rs.AddLayer(name=lname, color=None,
                            visible=True, locked=False, parent=parent)
        layer_id = rs.LayerId(lname)
        # move layer under parent layer
        rs.ParentLayer(layer=lname, parent=parent)
        # fullpath layername
        lname = rs.LayerName(layer_id=layer_id, fullpath=True)
    else:
        layer_id = rs.LayerId("{}::{}".format(parent, lname))
        lname = rs.LayerName(layer_id)

    if attr:
        set_layer_user_text(lname=lname, data=attr)

    return lname, layer_id


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
    set_document_user_text(data=project.attributes)

    # project layer
    project_lname, project_lid = add_child_layer(
        lname=project.project_id_string, parent=add_parent_layer('OpenPlans')[0])

    # plan layers
    plans = project.fetch_project_plans()
    for plan in plans:
        _plan_lname, _plan_lid = add_child_layer(
            lname=plan.plan_id_string, parent=project_lname, attr=plan.attributes)

    # polygon layers
        _polygon_layers = add_polygon_rhino_layers(plan)


def rhino_layers_to_project():
    """Read rhino objects (geometry and layers) from 
    rhino doc and construct 'OpenPlansProject' instance.

    Parameters
    ----------
    None

    Returns
    -------
    project :class: 'OpenPlansProject'
        Open Plans Project class instance
    """
    project = datamodels.OpenPlansProject.from_custom(
        data=get_document_user_text())

    project_layer = rs.LayerChildren("OpenPlans")[0]  # TODO: make more robust

    for plan_layer in rs.LayerChildren(project_layer):
        plan = datamodels.OpenPlansPlan.from_custom(
            data=get_layer_user_text(lname=plan_layer))

        for polygon_layer in rs.LayerChildren(plan_layer):
            rh_objs = sc.doc.Objects.FindByLayer(
                get_rhino_doc_layer_obj(polygon_layer))

            for obj in rh_objs:
                plan.add_polygon(
                    datamodels.OpenPlansPolygon.from_rhino_object(rhobj=obj.Id))

        project.add_plan(plan)

    return project


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
        lname, lid = add_child_layer(lname=' '.join(
            map(str, polygon.tags)), parent=rs.LayerName(plan.plan_id_string, fullpath=True))
        p_layers.append(lname)
        # add geometry to layer
        polygon_to_rhino_layer(
            geom=polygon.rhino_polygon(), layer=lname, attr=polygon.attributes)

    return p_layers


def polygon_to_rhino_layer(polygon, layer, attr=None):
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
    obj = rs.AddPolyline(polygon.points)
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


def get_object_user_text(object_id):
    return {k: json.loads(rs.GetUserText(object_id=object_id, key=k)) for k in rs.GetUserText(object_id=object_id)}


def set_layer_user_text(lname, data):
    index = sc.doc.Layers.FindByFullPath(lname, -1)
    if index >= 0:
        layer = sc.doc.Layers[index]
        if layer:
            for key, value in data.iteritems():
                layer.SetUserString(key, json.dumps(value))
            layer.CommitChanges()
    else:
        print('Error set layer text: Layer not found')


def get_layer_user_text(lname):
    index = sc.doc.Layers.FindByFullPath(lname, -1)
    if index >= 0:
        layer = sc.doc.Layers[index]
        if layer:
            return {k: json.loads(layer.GetUserString(key=k)) for k in layer.GetUserStrings().AllKeys}
    else:
        print('Error get layer text: Layer not found')


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


def get_rhino_doc_layer_obj(fullpath_lname):
    index = sc.doc.Layers.FindByFullPath(fullpath_lname, -1)
    if index >= 0:
        return sc.doc.Layers[index]


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
