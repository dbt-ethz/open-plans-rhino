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
    with open(filepath, 'w') as o:
        json.dump(data, o, indent=4)


def read_project_from_doc():
    project = datamodels.OpenPlansProject.from_custom(
        data=rhh.get_document_user_text())
    project_layer = rs.LayerChildren("OpenPlans")[0]

    for plan_layer in rs.LayerChildren(project_layer):
        plan = datamodels.OpenPlansPlan.from_custom(
            data=rhh.get_layer_user_text(lname=plan_layer))

        for polygon_layer in rs.LayerChildren(plan_layer):
            rh_objs = sc.doc.Objects.FindByLayer(
                rhh.get_rhino_doc_layer_obj(polygon_layer))

            for obj in rh_objs:
                plan.add_polygon(
                    datamodels.OpenPlansPolygon.from_rhino_object(rhobj=obj.Id))

        project.add_plan(plan)
    
    return project


def run_command(is_interactive):
    file_path = get_file_location()
    if file_path:
        project = read_project_from_doc()
        export_json(data=project.project, filepath=file_path)


if __name__ == "__main__":
    run_command(True)
