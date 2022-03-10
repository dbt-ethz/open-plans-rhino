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

import rhino.rhino_helpers as rhh
import datamodels


__commandname__ = "OPAddPlanToProject"


class AddPlan(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: add floor plan'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

        # create dropwdown for existing projects
        self.m_label_project = forms.Label(Text='Project')
        # Create Dropdown List
        self.m_dropdown_projects = forms.DropDown()
        # set projects in layers as options in dropdown
        self.m_dropdown_projects.DataStore = [project.split(
            '::')[1] for project in rs.LayerChildren("OpenPlans")]
        # set default value
        self.m_dropdown_projects.SelectedIndex = 0

        # create attributes type
        self.m_label_type = forms.Label(Text='Type')
        self.m_textbox_type = forms.TextBox(Text='floorplan')

        # create attributes architects
        self.m_label_floor = forms.Label(Text='floor level')
        self.m_textbox_floor = forms.TextBox(Text='0')

        # Create the default button
        self.DefaultButton = forms.Button(Text='Add')
        self.DefaultButton.Click += self.on_OK_button_click

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_close_button_click

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(80, 20)
        layout.AddRow(self.m_label_project, self.m_dropdown_projects)
        layout.AddRow(self.m_label_type, self.m_textbox_type)
        layout.AddRow(self.m_label_floor, self.m_textbox_floor)
        layout.AddRow(None)  # spacer
        layout.AddRow(self.AbortButton, self.DefaultButton)

        self.Content = layout

    # Get the value of the textbox
    def get_text(self):
        return {
            'type': self.m_textbox_type.Text,
            'floor': self.m_textbox_floor.Text
        }

    def get_project(self):
        # return self.m_dropdown_projects.DataStore[self.m_dropdown_projects.SelectedIndex]
        return self.m_dropdown_projects.SelectedIndex

    # Close button click handler
    def on_close_button_click(self, sender, e):
        self.Close(False)

    # OK button click handler
    def on_OK_button_click(self, sender, e):
        self.Close(True)


# The script that will be using the dialog.
def request_new_plan():
    dialog = AddPlan()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.get_text(), dialog.get_project()
    else:
        return None, None


@rhh.op_project_exists
def RunCommand():
    #ret = rhh.add_background_bitmap()
    ret = Rhino.Commands.Result.Success
    if ret == Rhino.Commands.Result.Success:
        plan, project = request_new_plan()
        if plan:
            # plan instance from user input
            plan = datamodels.OpenPlansPlan.from_custom(data=plan)

            # plan layer
            plan_lname, plan_lid = rhh.add_child_layer(lname=plan.plan_id_string,
                                            parent=rs.LayerChildren(
                                                "OpenPlans")[project],
                                            attr=plan.attributes)

            # TODO: Remove plan from document user text
            # project instance from document user data
            # project = datamodels.OpenPlansProject.from_custom(
            #     data=rhh.get_document_user_text())
            # # add plan and add to rhino
            # rhh.project_to_rhino_layers(project.add_plan(plan))


if __name__ == "__main__":
    RunCommand(True)
