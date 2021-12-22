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
from decorators import projectcheck


__commandname__ = "OPTagPlanPolygon"


class PolygonTagSelection(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self, polygonLayer):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: tag polygon'
        self.Padding = drawing.Padding(10)
        self.Resizable = False
        self.CurrentLayer = polygonLayer

        # Current project
        self.m_label_project = forms.Label(Text='Current Project:')
        self.m_textbox_project = forms.Label(
            Text=self.CurrentLayer.split("::")[1])

        # Current floor
        self.m_label_floor = forms.Label(Text='Floor:')
        self.m_textbox_floor = forms.Label(
            Text=self.CurrentLayer.split("::")[2])

        # Create Combobox
        self.m_label = forms.Label(Text='Tag:')
        self.m_combobox = forms.ComboBox()
        self.m_combobox.DataStore = ['building', 'wall']

        # Create the default button
        self.DefaultButton = forms.Button(Text='OK')
        self.DefaultButton.Click += self.OnOKButtonClick

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.OnCloseButtonClick

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(80, 20)
        layout.AddRow(self.m_label_project, self.m_textbox_project)
        layout.AddRow(self.m_label_floor, self.m_textbox_floor)
        layout.AddRow(self.m_label, self.m_combobox)
        layout.AddRow(None)  # spacer
        layout.AddRow(self.DefaultButton, self.AbortButton)

        # Set the dialog content
        self.Content = layout

    # Get the value of the textbox
    def GetText(self):
        return self.m_combobox.Text

    # Close button click handler
    def OnCloseButtonClick(self, sender, e):
        self.Close(False)

    # OK button click handler
    def OnOKButtonClick(self, sender, e):
        if self.m_combobox.Text == "":
            print("Failed to add tag: No tag is given")
            self.Close(False)
        else:
            self.Close(True)


# The script that will be using the dialog.
def RequestPolygonTag(polygonLayer):
    dialog = PolygonTagSelection(polygonLayer=polygonLayer)
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.GetText()


def RequestPolygon():
    # get a polyline
    obj = rs.GetObject("Select a polygon to tag")
    rs.SelectObject(obj, redraw=False)
    return obj


def AddPolygon2Layer(obj, layer):
    rs.ObjectLayer(obj, layer=layer)


def CheckObjectLayer(obj_layer):
    # check if object is in the right layer depth
    if len(obj_layer.split('::')) == 3:
        # check if layer is part of a plan/floor
        if obj_layer.split('::')[-1].split('_')[1] == 'floor':
            return True, "Correct"
        else:
            return False, "Layer structure is not correct: Please check your layer names"
    # check if object already has a tag
    elif len(obj_layer.split('::')) == 4:
        return False, 'Polygon is already tagged'
    # other cases
    else:
        return False, "Polygon is not part of a Plan: Please assign your polygons to the correct layer"


@projectcheck
def RunCommand(is_interactive):
    # get a polyline
    obj = RequestPolygon()
    obj_layer = rs.ObjectLayer(obj)
    # check if object is in correct layer depth
    proceed, e = CheckObjectLayer(obj_layer)
    if proceed is True:
        # if no tag exists and object is in correct layer, tag can be assigned
        tag = RequestPolygonTag(polygonLayer=obj_layer)
        if tag:
            layer = AddChildLayer(tag, parent=obj_layer)
            AddPolygon2Layer(obj, layer)
    else:
        print(e)


if __name__ == "__main__":
    RunCommand(True)
