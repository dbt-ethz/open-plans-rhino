from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from datamodels.project_class import OpenPlansProject

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
import System
import Rhino.UI
import Eto.Forms as forms
import Eto.Drawing as drawing

import rhino.rhino_helpers as rhh
import datamodels
import json


__commandname__ = "OPUploadProject"


class GetJsonFilePath(forms.Dialog[bool]):

    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: Upload project to database'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

        # select file location
        self.m_label_file = forms.Label(Text='Project File Path (json)')
        self.m_textbox_file = forms.TextBox(Text=None)

        # Create the browse button
        self.BrowseButton = forms.Button(Text='Browse...')
        self.BrowseButton.Click += self.on_browse_button_click

        # Create the default button
        self.DefaultButton = forms.Button(Text='Upload')
        self.DefaultButton.Click += self.on_OK_button_click

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_close_button_click

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(80, 20)
        layout.AddRow(self.m_label_file,
                      self.m_textbox_file, self.BrowseButton)
        layout.AddRow(self.m_label_file,
                      self.m_textbox_file, self.BrowseButton)
        layout.AddRow(None)  # spacer
        layout.AddRow(None, self.DefaultButton, self.AbortButton)

        self.Content = layout

    def get_file_location(self):
        return self.m_textbox_file.Text

    # Close button click handler

    def on_close_button_click(self, sender, e):
        self.Close(False)

    # OK button click handler
    def on_OK_button_click(self, sender, e):
        if self.m_textbox_file.Text == "":
            raise Exception("Failed to upload project: file path is required")
        else:
            self.Close(True)

    def on_browse_button_click(self, sender, e):
        filename = rs.OpenFileName("Open", "JSON Files (*.json)|*.json||")
        if filename:
            self.m_textbox_file.Text = filename


def request_json_file():
    dialog = GetJsonFilePath()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.get_file_location()
    else:
        return False


def json_to_dict(filepath):
    with open(filepath) as d:
        data = json.load(d)
    if data:
        return data


def RunCommand(is_interactive):
    project_file = request_json_file()
    data = json_to_dict(project_file)
    project = datamodels.OpenPlansProject.from_custom(data=data)
    # project.upload_to_openplans()


if __name__ == "__main__":
    RunCommand(True)
