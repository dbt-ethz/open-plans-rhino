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


def get_file_location():
    return rs.OpenFileName("Open", "JSON Files (*.json)|*.json||")


def export_json(data, filepath):
    with open(filepath, 'w') as o:
        json.dump(data, o, indent=4)


def run_command(is_interactive):
    file_path = get_file_location()
    if file_path:
        project = rhh.rhino_layers_to_project()
        export_json(data=project.project, filepath=file_path)
        print("Export json to: ", file_path)


if __name__ == "__main__":
    run_command(True)
