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


def remove_none_values(data):
    """
    Given a dictionary, dict, remove None values
    If the dictionary includes nested dictionaries, investigate and remove None values there too.
    """
    cleaned_dict = {}
    for key, value in data.iteritems():
        if type(value) is list:
            nested_list = []
            for i in value:
                if type(i) is dict:
                    nested_dict = remove_none_values(i)
                    if len(nested_dict.keys()) > 0:
                        nested_list.append(nested_dict)
                elif value:
                    nested_list.append(i)

            if len(nested_list) > 0:
                cleaned_dict[key] = nested_list

        elif value:
            cleaned_dict[key] = value

    return cleaned_dict


def run_command(is_interactive):
    project = rhh.rhino_layers_to_project()
    project = remove_none_values(project.project)
    resp = api.save_project(project)
    print("Project succesfully uploaded to the Open Plans database")


if __name__ == "__main__":
    run_command(True)
