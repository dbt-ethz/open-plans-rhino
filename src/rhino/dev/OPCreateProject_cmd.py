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
import datamodels as models
import api

__commandname__ = "OPCreateProject"


class CreateProject(forms.Dialog[bool]):

    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: Create New Project'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

        # create attributes Name
        self.m_label_name = forms.Label(Text='Project Name')
        self.m_textbox_name = forms.TextBox(Text=None)

        # create attributes architects
        self.m_label_architect = forms.Label(
            Text='Architect(s) (separate architects with ",")')
        self.m_textbox_architect = forms.TextBox()

        # create attributes civil engineer
        self.m_label_ceng = forms.Label(Text='Civil Engineer')
        self.m_textbox_ceng = forms.TextBox(Text=None)

        # create attributes client
        self.m_label_client = forms.Label(Text='Client')
        self.m_textbox_client = forms.TextBox(Text=None)

        # create attributes year of completion
        self.m_label_yoc = forms.Label(Text='Year of Completion')
        self.m_numeric_yoc = forms.TextBox()
        self.m_numeric_yoc.MaxLength = 4
        self.m_numeric_yoc.PlaceholderText = '1990'

        # create description multiline textbox
        self.m_label_richtext = forms.Label(Text='Project description')
        self.m_richtextarea = forms.RichTextArea()
        self.m_richtextarea.Size = drawing.Size(210, 100)

        # create attributes source
        self.m_label_source = forms.Label(Text='Source information')
        self.m_textbox_source = forms.TextBox(Text=None)

        # Create the default button
        self.DefaultButton = forms.Button(Text='Create')
        self.DefaultButton.Click += self.on_OK_button_click

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_close_button_click

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(100, 10)
        layout.AddRow(self.m_label_name, self.m_textbox_name)
        layout.AddRow(self.m_label_architect, self.m_textbox_architect)
        layout.AddRow(self.m_label_ceng, self.m_textbox_ceng)
        layout.AddRow(self.m_label_client, self.m_textbox_client)
        layout.AddRow(self.m_label_source, self.m_textbox_source)
        layout.AddRow(self.m_label_yoc, self.m_numeric_yoc)
        layout.AddRow(self.m_label_richtext, self.m_richtextarea)
        layout.AddRow(None)  # spacer
        layout.AddRow(self.AbortButton, self.DefaultButton)

        self.Content = layout

    # Get the value of the textbox
    def get_text(self):
        return {
            'name': self.m_textbox_name.Text,
            'architects': self.m_textbox_architect.Text,
            'civil_engineer': self.m_textbox_ceng.Text,
            'client': self.m_textbox_client.Text,
            'year_of_completion': self.m_numeric_yoc.Text,
            'source': self.m_textbox_source.Text,
            'description': self.m_richtextarea.Text
        }

    # Close button click handler

    def on_close_button_click(self, sender, e):
        self.Close(False)

    # OK button click handler
    def on_OK_button_click(self, sender, e):
        if self.m_textbox_name.Text == "":
            print("Failed to create project: Name is required")
            self.Close(False)
        else:
            self.Close(True)


def request_new_project():
    dialog = CreateProject()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.get_text()


def create_new_project(project):
    empty_project = models.ProjectData()
    # modify empty project template with new project data
    new = empty_project.modify_project(field_changes=project)
    # upload project to OP database
    #project_id = new.save_project_to_openplans()
    project_id = 557
    # retrieve project from open plans database
    if project_id:
        resp = api.fetch_project(project_id=project_id)
        if resp['succeeded']:
            return models.ProjectData(project=resp['project'])
        else:
            print(resp['error'])


def run_command(is_interactive):
    new_project = request_new_project()

    if new_project:
        openplans_project = create_new_project(new_project)
        # add project to rhino layers
        rhh.project_to_rhino_layers(openplans_project)


if __name__ == "__main__":
    run_command(True)
