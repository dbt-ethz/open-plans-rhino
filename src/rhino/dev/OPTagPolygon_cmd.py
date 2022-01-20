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


__commandname__ = "OPTagPlanPolygon"


class PolygonTagSelection(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self, polygon_layer):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: tag polygon'
        self.Padding = drawing.Padding(10)
        self.Resizable = False
        self.CurrentLayer = polygon_layer

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
        self.DefaultButton.Click += self.on_OK_button_click

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_close_button_click

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
    def get_text(self):
        return self.m_combobox.Text

    # Close button click handler
    def on_close_button_click(self, sender, e):
        self.Close(False)

    # OK button click handler
    def on_OK_button_click(self, sender, e):
        if self.m_combobox.Text == "":
            print("Failed to add tag: No tag is given")
            self.Close(False)
        else:
            self.Close(True)


# The script that will be using the dialog.
def request_polygon_tag(layer):
    dialog = PolygonTagSelection(polygon_layer=layer)
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.get_text()


def request_polygon():
    # get a polyline
    obj = rs.GetObject("Select a polygon to tag")
    rs.SelectObject(obj, redraw=False)
    return obj


@rhh.op_project_exists
def run_command():
    # get a polyline
    obj = request_polygon()
    obj_layer = rs.ObjectLayer(obj)

    # if no tag exists and object is in correct layer, tag can be assigned
    tag = request_polygon_tag(layer=obj_layer)
    if tag:
        layer = rhh.add_child_layer(tag, parent=obj_layer)
        rs.ObjectLayer(obj, layer=layer)
        pts_data = rhh.rhino_curve_to_data_points(obj)
        polygon = datamodels.OpenPlansPolygon.from_custom(
            data={'points': pts_data, 'tags': [tag]})
        
        rhh.set_object_user_text(object_id=obj, data=polygon.polygon)


if __name__ == "__main__":
    run_command(True)
