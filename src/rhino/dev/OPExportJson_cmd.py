from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
import System
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms

import datamodels
import rhino.rhino_helpers as rhh

import json

__commandname__ = "OPExportJson"


def get_file_location():
    return rs.OpenFileName("Open", "JSON Files (*.json)|*.json||")


def export_json(data, filepath):
    pass


def get_object_user_text(object_id):
    return {k: json.loads(rs.GetUserText(object_id=object_id, key=k)) for k in rs.GetUserText(object_id=object_id)}


def read_project_from_doc():
    project = datamodels.OpenPlansProject.from_custom(
        data=rhh.get_document_user_text())
    project_layer = rs.LayerChildren("OpenPlans")[0]
    for plan_layer in rs.LayerChildren(project_layer):
        plan = datamodels.OpenPlansPlan.from_custom(
            data=rhh.get_layer_user_text(lname=plan_layer))
        print(plan)
        for polygon_layer in rs.LayerChildren(plan_layer):
            print(polygon_layer)
            rh_objs = sc.doc.Objects.FindByLayer(
                get_rhino_doc_layer_obj(polygon_layer))
            for obj in rh_objs:
                pts_data = rhh.rhino_curve_to_data_points(obj.Id)
                data = get_object_user_text(object_id=obj.Id)
                data['points'] = pts_data
                polygon = datamodels.OpenPlansPolygon.from_custom(data)
                print(polygon.polygon)


def get_rhino_doc_layer_obj(fullpath_lname):
    index = sc.doc.Layers.FindByFullPath(fullpath_lname, -1)
    if index >= 0:
        return sc.doc.Layers[index]


def run_command(is_interactive):
    file_path = get_file_location()
    if file_path:
        print(file_path)
        read_project_from_doc()


if __name__ == "__main__":
    run_command(True)
