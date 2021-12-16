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
    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: tag polygon'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

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
        layout.Spacing = drawing.Size(5, 5)
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
        self.m_textbox.Text = ""
        self.Close(False)

    # OK button click handler
    def OnOKButtonClick(self, sender, e):
        if self.m_combobox.Text == "":
            self.Close(False)
        else:
            self.Close(True)

   
# The script that will be using the dialog.
def RequestPolygonTag():
    dialog = PolygonTagSelection();
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.GetText()


def AddTagLayer(tag):
    # Parent layer: Open Plans
    if rs.IsLayer('OpenPlans'):
        rs.CurrentLayer("OpenPlans")
    else:
        rs.AddLayer(name='OpenPlans', color=None, visible=True, locked=False, parent=None)
        rs.CurrentLayer("OpenPlans")
    
    # Add layer for new tag
    if rs.IsLayer(tag):
        tag_layer = rs.LayerId(tag)
    else:
        layer = rs.AddLayer(name=tag, color=None, visible=True, locked=False, parent="OpenPlans")
        tag_layer = rs.LayerId(layer)

    return tag_layer


def AddPolygon2Layer(obj, layer):
    rs.ObjectLayer(obj, layer=layer)
    

def RunCommand( is_interactive ):
    # get a polygline
    obj = rs.GetObject("Select a polygon to tag")
    rs.SelectObject(obj, redraw=False)
    
    tag = RequestPolygonTag()
    
    layer = AddTagLayer(tag)
    AddPolygon2Layer(obj, layer)
    

if __name__ == "__main__":
    RunCommand(True)