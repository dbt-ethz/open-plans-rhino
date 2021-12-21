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

from auth import Login, checkLoginStatus


__commandname__ = "OPMyAccount"


class AccountInfo(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: My Account'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

        self.LoginStatus = self.getLoginStatus()
        # Satus Groupbox
        self.m_groupbox_status = forms.GroupBox(Text='Account Status')
        self.m_groupbox_status.Padding = drawing.Padding(5)
        # layout
        grouplayout_status = forms.DynamicLayout()
        grouplayout_status.Spacing = drawing.Size(200, 20)
        # email
        label_status = forms.Label(Text='Active Account:')
        box_status = forms.Label(Text=str(self.LoginStatus))
        # logout button
        self.SignOutButton = forms.Button(Text='Sign out')
        self.SignOutButton.Click += self.OnSignOutButtonClick
        self.SignOutButton.Enabled = self.LoginStatus
        # add to layout
        grouplayout_status.AddRow(label_status, box_status)
        grouplayout_status.AddRow(None, self.SignOutButton)
        self.m_groupbox_status.Content = grouplayout_status

        # Login Groupbox
        self.m_groupbox_login = forms.GroupBox(Text='Sign in')
        self.m_groupbox_login.Padding = drawing.Padding(5)
        # layout
        grouplayout_login = forms.DynamicLayout()
        grouplayout_login.Spacing = drawing.Size(200, 20)
        # email
        label_email_login = forms.Label(Text='Email:')
        textbox_email_login = forms.TextBox()
        # password
        label_pw_login = forms.Label(Text='Password:')
        passwordbox_pw_login = forms.PasswordBox()
        # check for account existinf
        checkbox_new = forms.CheckBox(Text='Create New Account')
        # login button
        self.LoginButton = forms.Button(Text='Sign in')
        self.LoginButton.Click += self.OnLoginButtonClick
        # add to layout
        grouplayout_login.AddRow(label_email_login, textbox_email_login)
        grouplayout_login.AddRow(label_pw_login, passwordbox_pw_login)
        grouplayout_login.AddRow(checkbox_new, self.LoginButton)
        self.m_groupbox_login.Content = grouplayout_login

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.OnCloseButtonClick

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(200, 20)
        layout.AddRow(self.m_groupbox_status)
        layout.AddRow(self.m_groupbox_login)
        layout.AddRow(None)  # spacer
        layout.AddRow(self.AbortButton)

        # Set the dialog content
        self.Content = layout

    # Get the value of the textbox
    def GetText(self):
        return self.m_combobox.Text

    # Close button click handler
    def OnCloseButtonClick(self, sender, e):
        self.Close(False)

    # OK button click handler
    def OnLoginButtonClick(self, sender, e):
        if self.m_combobox.Text == "":
            print("Failed to add tag: No tag is given")
            self.Close(False)
        else:
            self.Close(True)

    # signout button click handler
    def OnSignOutButtonClick(self, sender, e):
        if self.m_combobox.Text == "":
            print("Failed to add tag: No tag is given")
            self.Close(False)
        else:
            self.Close(True)

    @staticmethod
    def getLoginStatus():
        return checkLoginStatus()['is_logged']


# The script that will be using the dialog.
def RequestAccount():
    dialog = AccountInfo()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.GetText()


def RunCommand(is_interactive):
    RequestAccount()


if __name__ == "__main__":
    RunCommand(True)
