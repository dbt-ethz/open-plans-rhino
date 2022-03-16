from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
import System
import Rhino.UI

import rhino.rhino_helpers as rhh
import api
import json

__commandname__ = "OPUploadProject"


def RunCommand(is_interactive):
    project = rhh.rhino_layers_to_project()
    plan_objs = project.plan_objs()
    plan_objs_new = [plan.add_image_data(test=True) for plan in plan_objs]
    plans = [p.plan for p in plan_objs_new]
    project.modify_project(plans=plans)
    #print(project.project)
    project.upload_to_openplans()


if __name__ == "__main__":
    RunCommand(True)
