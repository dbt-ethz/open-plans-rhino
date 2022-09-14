from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import Rhino
import scriptcontext as sc
import System.Windows.Forms.DialogResult
import System.Drawing.Image
import json

import datamodels


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


def remove_empty_layer(lname):
    if rs.IsLayer(lname):
        if rs.IsLayerEmpty(lname):
            rs.DeleteLayer(lname)


def project_to_rhino_layers(project, plan_ids=None):
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
    if plan_ids:
        plans = project.fetch_project_plans(plan_ids=plan_ids)
    else:
        plans = project.fetch_project_plans()
    for plan in plans:
        _plan_lname, _plan_lid = add_child_layer(
            lname=plan.plan_id_string, parent=project_lname, attr=plan.attributes)

    # polygon layers
        _polygon_layers = add_polygon_rhino_layers(plan)


def rhino_layers_to_project(frame_size=None, plan_layer_selection=None):
    """Read rhino objects (geometry and layers) from 
    rhino doc and construct 'OpenPlansProject' instance.

    Parameters
    ----------
    frame_size: tuple
        w, h of image frame

    Returns
    -------
    project :class: 'OpenPlansProject'
        Open Plans Project class instance
    """
    project = datamodels.OpenPlansProject.from_custom(
        data=get_document_user_text())

    project_layer = rs.LayerChildren("OpenPlans")[0]  # TODO: make more robust
    plan_layers = rs.LayerChildren(project_layer)
    if plan_layer_selection:
        plan_layers = [plan for plan in rs.LayerChildren(project_layer) if plan in plan_layer_selection]

    for plan_layer in plan_layers:
        plan = datamodels.OpenPlansPlan.from_custom(
            data=get_layer_user_text(lname=plan_layer))
        if frame_size:
            plan.set_image_size(frame_size)

        for polygon_layer in rs.LayerChildren(plan_layer):
            rh_objs = sc.doc.Objects.FindByLayer(
                get_rhino_doc_layer_obj(polygon_layer))

            for obj in rh_objs:
                # TODO: change frame_size to plan.height_mm
                plan.add_polygon(
                    datamodels.OpenPlansPolygon.from_rhino_object(rhobj=obj.Id, frame_size=frame_size))

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
    for polygon in plan.plan_polygon_objs():
        lname, lid = add_child_layer(lname='{} ({})'.format(', '.join(
            map(str, polygon.tags)), plan.plan_id_string.split(' ')[0]), parent=rs.LayerName(plan.plan_id_string, fullpath=True))
        p_layers.append(lname)
        # add geometry to layer
        polygon_to_rhino_layer(
            polygon=polygon.rhino_polygon(frame_height=plan.height_mm), layer=lname, attr=polygon.attributes)

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
    try:
        return {k: json.loads(rs.GetDocumentUserText(key=k)) for k in rs.GetDocumentUserText()}
    except:
        print("Invalid characters in document user text. Please check strings are quoted with ''")


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


def get_active_project():
    return datamodels.OpenPlansProject.from_custom(
        data=get_document_user_text())


def get_active_plan_layernames(fullpath=True):
    project = get_active_project()
    if fullpath:
        return rs.LayerChildren(project.project_id_string)
    else:
        return [floor.split(
            '::')[2] for floor in rs.LayerChildren(project.project_id_string)]


def rhino_curve_to_data_points(obj, frame_size):
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
    if frame_size:
        return [{'x': p.X, 'y': (p.Y - frame_size[1]) * -1} for p in points]
    else:
        return [{'x': p.X, 'y': p.Y} for p in points]


def get_rhino_doc_layer_obj(fullpath_lname):
    index = sc.doc.Layers.FindByFullPath(fullpath_lname, -1)
    if index >= 0:
        return sc.doc.Layers[index]


def snap_image(size, mms_per_pixel=10):
    Rhino.RhinoApp.RunScript(
        "_SetZoomExtentsBorder _ParallelView=1 _Enter", True)

    x, y = size[0], size[1]
    blc_pt = rg.Point3d(x, y, 0)
    pts = [rg.Point3d(0, 0, 0), blc_pt]
    bb = rg.BoundingBox(pts)
    RhinoDocument = Rhino.RhinoDoc.ActiveDoc
    view = RhinoDocument.Views.Find("Top", False)
    vp = view.ActiveViewport
    width, height = x / mms_per_pixel, y / mms_per_pixel
    size = System.Drawing.Size(width, height)
    vp.Size = size
    view.Redraw()
    vp.ZoomBoundingBox(bb)
    capture = view.CaptureToBitmap(size, False, False, False)
    return capture


def set_frame():
    rect = rs.GetRectangle(
        mode=1, base_point=(0, 0, 0),
        prompt1="Please draw a frame around your flooplan",
        prompt2="Please draw a frame around your flooplan. This frame is used to take an image and defines the coordinate system"
    )
    if rect:
        print(rect)
        w = int(abs(rect[1].X - rect[0].X))
        h = int(abs(rect[3].Y - rect[0].Y))
        return (w, h)


def add_background_bitmap():
    # Allow the user to select a bitmap file
    fd = Rhino.UI.OpenFileDialog()
    fd.Filter = "Image Files (*.bmp;*.png;*.jpg)|*.bmp;*.png;*.jpg"
    if not fd.ShowDialog():
        return Rhino.Commands.Result.Cancel

    # Verify the file that was selected
    image = None
    try:
        image = System.Drawing.Image.FromFile(fd.FileName)
    except:
        return Rhino.Commands.Result.Failure

    # Allow the user to pick the bitmap origin
    gp = Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("Bitmap Origin")
    gp.ConstrainToConstructionPlane(True)
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return gp.CommandResult()

    # Get the view that the point was picked in.
    # This will be the view that the bitmap appears in.
    view = gp.View()
    if view is None:
        view = sc.doc.Views.ActiveView
        if view is None:
            return Rhino.Commands.Result.Failure

    plane = view.ActiveViewport.ConstructionPlane()
    plane.Origin = gp.Point()
    view.ActiveViewport.SetTraceImage(
        fd.FileName, plane, image.Width, image.Height, False, False)
    view.Redraw()
    return Rhino.Commands.Result.Success


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
