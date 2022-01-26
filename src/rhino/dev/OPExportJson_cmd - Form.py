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

import api
import datamodels as models

__commandname__ = "OPExportJson"


class ExportJson(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: Export Project to JSON'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

        # select file location
        self.m_label_file = forms.Label(Text='Save File Path')
        self.m_textbox_file = forms.TextBox(Text=None)

        # Create the browse button
        self.BrowseButton = forms.Button(Text='Browse...')
        self.BrowseButton.Click += self.on_browse_button_click

        # Create the default button
        self.DefaultButton = forms.Button(Text='Export')
        self.DefaultButton.Click += self.on_OK_button_click

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_close_button_click

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(5, 5)

        layout.AddRow('Project File Location:')

        layout.BeginVertical()
        layout.AddRow(self.m_textbox_file, self.BrowseButton)
        layout.EndVertical()


        layout.BeginVertical()
        layout.AddRow(None, self.AbortButton, self.DefaultButton, None)
        layout.EndVertical()
        #layout.AddSeparateRow(None, self.AbortButton, self.DefaultButton, None)
        #layout.AddSeparateRow(self.AbortButton)

        self.Content = layout

    # Get the value of the textbox
    def get_file_location(self):
        return self.m_textbox_file.Text

    # Close button click handler
    def on_close_button_click(self, sender, e):
        self.Close(False)

    # OK button click handler
    def on_OK_button_click(self, sender, e):
        if self.m_textbox_name.Text == "":
            self.Close(False)
        else:
            self.Close(True)

    def on_browse_button_click(self, sender, e):
        filename = rs.OpenFileName("Open", "JSON Files (*.json)|*.json||")
        if filename:
            self.m_textbox_file.Text = filename



# The script that will be using the dialog.
def request_account():
    dialog = ExportJson()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.get_file_location()


def run_command(is_interactive):
    file_path = request_account()
    if file_path:
        pass


if __name__ == "__main__":
    run_command(True)
