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


def run_command(is_interactive):
    project = rhh.rhino_layers_to_project()
    project.upload_to_openplans()


if __name__ == "__main__":
    run_command(True)
