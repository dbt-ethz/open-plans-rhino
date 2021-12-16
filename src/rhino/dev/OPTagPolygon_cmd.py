import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import System
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms


__commandname__ = "TagPlanPolygon"

class PolygonTagSelection(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self, polygonLayer):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: tag polygon'
        self.Padding = drawing.Padding(10)
        self.Resizable = False
        self.CurrentLayer = polygonLayer

        #Current project
        self.m_label_project = forms.Label(Text = 'Current Project:')
        self.m_textbox_project = forms.Label(Text = self.CurrentLayer.split("::")[1])

        #Current floor
        self.m_label_floor = forms.Label(Text = 'Floor:')
        self.m_textbox_floor = forms.Label(Text = self.CurrentLayer.split("::")[2])

        #Create Combobox
        self.m_label = forms.Label(Text = 'Tag:')
        self.m_combobox = forms.ComboBox()
        self.m_combobox.DataStore = ['building', 'wall']

        # Create the default button
        self.DefaultButton = forms.Button(Text = 'OK')
        self.DefaultButton.Click += self.OnOKButtonClick

        # Create the abort button
        self.AbortButton = forms.Button(Text = 'Cancel')
        self.AbortButton.Click += self.OnCloseButtonClick

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(80, 20)
        layout.AddRow(self.m_label_project, self.m_textbox_project)
        layout.AddRow(self.m_label_floor, self.m_textbox_floor)
        layout.AddRow(self.m_label, self.m_combobox)
        layout.AddRow(None) # spacer
        layout.AddRow(self.DefaultButton, self.AbortButton)

        # Set the dialog content
        self.Content = layout

    # Get the value of the textbox
    def GetText(self):
        return self.m_combobox.Text

    # Close button click handler
    def OnCloseButtonClick(self, sender, e):
        self.m_combobox.Text = ""
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
    dialog = PolygonTagSelection(polygonLayer=polygonLayer);
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.GetText()


def AddChildLayer(lname, parent):
    # Add layer for new project
    if rs.IsLayer(lname):
        return lname
    else:
        layer = rs.AddLayer(name=lname, color=None, visible=True, locked=False, parent=parent)
        rs.ParentLayer(layer=layer, parent=parent)
        return layer


def AddPolygon2Layer(obj, layer):
    rs.ObjectLayer(obj, layer=layer)
    

def RunCommand( is_interactive ):
    # get a polygline
    obj = rs.GetObject("Select a polygon to tag")
    rs.SelectObject(obj, redraw=False)
    obj_layer = rs.ObjectLayer(obj)
    
    tag = RequestPolygonTag(polygonLayer=obj_layer)

    if tag:    
        layer = AddChildLayer(tag, parent=obj_layer)
        AddPolygon2Layer(obj, layer)
    

if __name__ == "__main__":
    RunCommand(True)