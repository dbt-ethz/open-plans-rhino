from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
import datamodels

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
    return project


def CommandLineOptions():
    gp = Rhino.Input.Custom.GetOption()
    gp.SetCommandPrompt("Export project plan to JSON")
    gp.AcceptNothing(True)

    plan_layers_full = rhh.get_active_plan_layernames(fullpath=True)
    plan_layers = [floor.split('::')[2] for floor in plan_layers_full]

    # set up the options
    boolOption = Rhino.Input.Custom.OptionToggle(True, "No", "Yes")
    listValues = [plan.split(';')[0].replace(" ", "_") for plan in plan_layers]

    gp.AddOptionToggle("SetNewCoordinateFrame", boolOption)
    listIndex = 0
    opList = gp.AddOptionList("PlanToExport", listValues, listIndex)

    while True:

        get_rc = gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return None, None
        if get_rc == Rhino.Input.GetResult.Nothing:
            plan = plan_layers_full[listIndex]
            print("Export plan: ", plan_layers[listIndex])
            return plan, boolOption.CurrentValue
        if get_rc == Rhino.Input.GetResult.Option:
            if gp.OptionIndex() == opList:
                listIndex = gp.Option().CurrentListOptionIndex
            continue
        break
    return None, None


def RunCommand(is_interactive):
    export_plan_lname, set_frame_bool = CommandLineOptions()
    if not export_plan_lname:
        return 0

    if set_frame_bool:
        size = rhh.set_frame()
    else:
        layer_text = rhh.get_layer_user_text(lname=export_plan_lname)
        plan = datamodels.OpenPlansPlan.from_custom(data=layer_text)
        if (layer_text['image_path'] or layer_text['image_data']) and plan.width_mm:
            size = (plan.width_mm, plan.height_mm)
        else:
            print("Plan does not have a coordinate frame or image yet.")
            size = rhh.set_frame()
            set_frame_bool = True

    new_image = False
    if size:
        if set_frame_bool:
            image_file_path = get_file_location_image()
            if image_file_path:
                img = rhh.snap_image(size)
                try:
                    export_image(image=img, filepath=image_file_path)
                    print("Succesful export image to: ", image_file_path)
                    new_image = True
                except:
                    print("Failed to export: ", image_file_path)
                    return 0

        json_file_path = get_file_location_json()
        if json_file_path:
            project = rhh.rhino_layers_to_project(
                frame_size=size, plan_layer_selection=export_plan_lname)
            # add image data to plan
            if new_image:
                project = add_image_to_plan(project, image_file_path)
                # update layer user text
                new_plan = project.plan_objs()[0]
                rhh.set_layer_user_text(export_plan_lname, new_plan.plan)
                #TODO: Check plan id instead of id
            try:
                export_json(data=project.project, filepath=json_file_path)
                print("Succesful export json to: ", json_file_path)
            except:
                print("Failed to export: ", json_file_path)

    return Rhino.Commands.Result.Success

if __name__ == "__main__":
    RunCommand(True)
