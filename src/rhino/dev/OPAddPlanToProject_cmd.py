import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import System
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms


__commandname__ = "OPAddPlanToProject"

class AddPlan(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: add floor plan'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

        # create dropwdown for existing projects
        self.m_label_project = forms.Label(Text = 'Project')
        #Create Dropdown List
        self.m_dropdown_projects = forms.DropDown()
        projects = rs.LayerChildren("OpenPlans")
        # check if projects exist
        if projects:
            children = [ project.split('::')[1] for project in projects ]
        # else give error message and exit process
        else:
            print("Failed to add plan: Please create a project first (use OPCreateProject cmd)")
            self.Title = "Failed to add plan: Please create a project first with OPCreateProject"
            self.Padding = drawing.Padding(230, 10)
            return 0
        self.m_dropdown_projects.DataStore = children
        # set default value
        self.m_dropdown_projects.SelectedIndex = 0

        # create attributes type
        self.m_label_type = forms.Label(Text = 'Type')
        self.m_textbox_type = forms.TextBox(Text = 'floorplan')
        
        # create attributes architects
        self.m_label_floor = forms.Label(Text = 'floor level')
        self.m_textbox_floor = forms.TextBox(Text = '0')

        # Create the default button
        self.DefaultButton = forms.Button(Text = 'Add')
        self.DefaultButton.Click += self.OnOKButtonClick

        # Create the abort button
        self.AbortButton = forms.Button(Text = 'Cancel')
        self.AbortButton.Click += self.OnCloseButtonClick

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(80, 20)
        layout.AddRow(self.m_label_project, self.m_dropdown_projects)
        layout.AddRow(self.m_label_type, self.m_textbox_type)
        layout.AddRow(self.m_label_floor, self.m_textbox_floor)
        layout.AddRow(None) # spacer
        layout.AddRow(self.DefaultButton, self.AbortButton)

        self.Content = layout

    # Get the value of the textbox
    def GetText(self):
        return {
                'type':self.m_textbox_type.Text,
                'floor':self.m_textbox_floor.Text
                }

    def GetProject(self):
        return self.m_dropdown_projects.DataStore[self.m_dropdown_projects.SelectedIndex]

    # Close button click handler
    def OnCloseButtonClick(self, sender, e):
        self.Close(False)

    # OK button click handler
    def OnOKButtonClick(self, sender, e):
        self.Close(True)

def AddChildLayer(lname, parent):
    # Add layer for new project
    if rs.IsLayer(lname):
        return lname
    else:
        layer = rs.AddLayer(name=lname, color=None, visible=True, locked=False, parent=parent)
        rs.ParentLayer(layer=layer, parent=parent)
        return layer

# The script that will be using the dialog.
def RequestNewPlan():
    dialog = AddPlan();
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.GetText(), dialog.GetProject()


def RunCommand( is_interactive ):
    plan, project = RequestNewPlan()

    AddChildLayer(lname=plan['floor'].zfill(2) + '_floor', parent=project)
    

if __name__ == "__main__":
    RunCommand(True)