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

from helpers import AddChildLayer
from datamodels.ProjectClass import ProjectData

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
        self.DefaultButton.Click += self.OnOKButtonClick

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.OnCloseButtonClick

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
    def GetText(self):
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

    def OnCloseButtonClick(self, sender, e):
        self.Close(False)

    # OK button click handler
    def OnOKButtonClick(self, sender, e):
        if self.m_textbox_name.Text == "":
            print("Failed to create project: Name is required")
            self.Close(False)
        else:
            self.Close(True)


def RequestNewProject():
    dialog = CreateProject()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.GetText()


def AddParentLayer(lname):
    if rs.IsLayer(lname):
        return lname
    else:
        parent = rs.AddLayer(name=lname, color=None,
                             visible=True, locked=False, parent=None)
        rs.CurrentLayer(parent)
        return parent


def RunCommand(is_interactive):
    newProject = RequestNewProject()

    if newProject:
        project = ProjectData()
        project.modify_project(newProject)
        print(project.jsonStr())
        parent = AddParentLayer('OpenPlans')
        layer = AddChildLayer(lname=newProject['name'], parent=parent)


if __name__ == "__main__":
    RunCommand(True)
