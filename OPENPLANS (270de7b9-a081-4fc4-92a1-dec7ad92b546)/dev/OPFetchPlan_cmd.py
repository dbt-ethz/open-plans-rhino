from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import System
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import Rhino.Display as rd

import rhino.rhino_helpers as rhh
import datamodels
import urllib2


__commandname__ = "OPFetchPlan"


def fetch_plan_by_id(id):
    return datamodels.OpenPlansProject.from_project_id(id)


def fetch_project_by_id(id):
    return datamodels.OpenPlansProject.from_project_id(id)


def get_file_location_image():
    return rs.OpenFileName("File location for floorplan image", "JPEG Files (*.jpeg)|*.jpeg||")


def export_image(img_url, filepath):
    response = urllib2.urlopen(img_url)
    output = open(filepath, "wb")
    output.write(response.read())
    output.close()


def draw_image_plan(img_url, mms_per_pixel):
    # Rhino Bitmap
    bitmap = rd.DisplayBitmap.Load(img_url)

    fpath = get_file_location_image()

    if fpath:
        export_image(img_url, fpath)
        # get active view
        RhinoDocument = Rhino.RhinoDoc.ActiveDoc
        view = RhinoDocument.Views.Find("Top", False)

        plane = view.ActiveViewport.ConstructionPlane()

        # load image into Rhino view
        view.ActiveViewport.SetTraceImage(
            fpath, plane, bitmap.Size.Width * mms_per_pixel, bitmap.Size.Height * mms_per_pixel, True, False)
        view.Redraw()

    else:
        print('Background image can not be displayed. Please export image to your device')


def RunCommand(is_interactive):
    plan_id = rs.GetInteger("Plan id")

    if plan_id:
        plan = datamodels.OpenPlansPlan.from_plan_id(id=plan_id)
        project_id = plan.get_project_id()

        op_project = fetch_project_by_id(id=project_id)

        # add project to rhino layers
        rhh.project_to_rhino_layers(op_project, plan_ids=[plan_id])

        draw_image_plan(plan.image_path, mms_per_pixel=plan.mms_per_pixel)


if __name__ == "__main__":
    RunCommand(True)
