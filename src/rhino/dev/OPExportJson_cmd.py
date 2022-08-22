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

import rhino.rhino_helpers as rhh

import json

__commandname__ = "OPExportJson"


def get_file_location_json():
    return rs.OpenFileName("File location for json export", "JSON Files (*.json)|*.json||")


def get_file_location_image():
    return rs.OpenFileName("File location for floorplan image", "JPEG Files (*.jpeg)|*.jpeg||")


def export_json(data, filepath):
    with open(filepath, 'w') as o:
        json.dump(data, o, indent=4)


def export_image(image, filepath):
    image.Save(filepath)


def add_image_to_plan(project, filepath):
    plan_objs = project.plan_objs()
    plan_objs_new = [plan.add_image_data(
        img_path=filepath) for plan in plan_objs]
    plans = [p.plan for p in plan_objs_new]
    project.modify_project(plans=plans)


def RunCommand(is_interactive):
    size = rhh.set_frame()
    if size:
        image_file_path = get_file_location_image()
        if image_file_path:
            img = rhh.snap_image(size)
            try:
                export_image(image=img, filepath=image_file_path)
                print("Export image to: ", image_file_path, "succesful")
            except:
                print("Failed to export: ", image_file_path)
                return 0

        json_file_path = get_file_location_json()
        if json_file_path:
            project = rhh.rhino_layers_to_project(frame_size=size)
            # add image data to plan
            add_image_to_plan(project, image_file_path)
            try:
                export_json(data=project.project, filepath=json_file_path)
                print("Export json to: ", json_file_path, "succesful")
            except:
                print("Failed to export: ", json_file_path)


if __name__ == "__main__":
    RunCommand(True)
