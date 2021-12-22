from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import rhinoscriptsyntax as rs


def projectcheck(func):
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
