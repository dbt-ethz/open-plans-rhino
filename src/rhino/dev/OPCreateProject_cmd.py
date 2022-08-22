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
import json

import rhino.rhino_helpers as rhh
import datamodels
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

        # select file location
        self.m_label_file = forms.Label(Text='Save File Path')
        self.m_textbox_file = forms.TextBox(Text=None)

        # Create the browse button
        self.BrowseButton = forms.Button(Text='Browse...')
        self.BrowseButton.Click += self.on_browse_button_click

        # Create the default button
        self.DefaultButton = forms.Button(Text='Create')
        self.DefaultButton.Click += self.on_OK_button_click

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_close_button_click

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)

        layout.BeginVertical()
        layout.AddRow(self.m_label_name, self.m_textbox_name)
        layout.AddRow(self.m_label_architect, self.m_textbox_architect)
        layout.AddRow(self.m_label_ceng, self.m_textbox_ceng)
        layout.AddRow(self.m_label_client, self.m_textbox_client)
        layout.AddRow(self.m_label_source, self.m_textbox_source)
        layout.AddRow(self.m_label_yoc, self.m_numeric_yoc)
        layout.AddRow(self.m_label_richtext, self.m_richtextarea)
        layout.AddRow(self.m_label_file,
                      self.m_textbox_file, self.BrowseButton)
        layout.EndVertical()

        layout.AddSeparateRow(self.DefaultButton)
        layout.AddSeparateRow(self.AbortButton)

        self.Content = layout

    # Get the value of the textbox
    def get_text(self):
        return {
            'name': self.m_textbox_name.Text,
            'architects': self.m_textbox_architect.Text.split(','),
            'civil_engineers': self.m_textbox_ceng.Text,
            'clients': self.m_textbox_client.Text,
            'year_of_completion': self.m_numeric_yoc.Text,
            'source': self.m_textbox_source.Text,
            'description': self.m_richtextarea.Text
        }

    def get_file_location(self):
        return self.m_textbox_file.Text

    # Close button click handler

    def on_close_button_click(self, sender, e):
        self.Close(False)

    # OK button click handler
    def on_OK_button_click(self, sender, e):
        if self.m_textbox_name.Text == "":
            raise Exception("Failed to create project: Name is required")
        else:
            self.Close(True)

    def on_browse_button_click(self, sender, e):
        filename = rs.OpenFileName("Open", "JSON Files (*.json)|*.json||")
        if filename:
            self.m_textbox_file.Text = filename


def request_new_project():
    dialog = CreateProject()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.get_text(), dialog.get_file_location()
    else:
        return False, False


def create_new_project(project):
    # project_id = api.get_data(dict=api.save_project(
    #     project=datamodels.OpenPlansProject.from_custom(data=project).project), key='project_id')
    # project_id = 557    # hardcoded for testing
    project_id = None
    if project_id:
        return datamodels.OpenPlansProject.from_project_id(project_id)
    else:
        return datamodels.OpenPlansProject.from_custom(data=project)


def RunCommand(is_interactive):
    new_project, file = request_new_project()

    if new_project:
        openplans_project = create_new_project(new_project)
        # add project to rhino layers
        rhh.project_to_rhino_layers(openplans_project)

        if file:
            with open(file, 'w') as o:
                json.dump(openplans_project.project, o, indent=4)


if __name__ == "__main__":
    RunCommand(True)
