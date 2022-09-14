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


__commandname__ = "OPMyAccount"


class AccountInfo(forms.Dialog[bool]):

    # Dialog box Class initializer
    def __init__(self):
        # Initialize dialog box
        self.Title = 'OPEN PLANS: My Account'
        self.Padding = drawing.Padding(10)
        self.Resizable = False

        self.LoginStatus = self.get_login_status()
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
        self.SignOutButton.Click += self.on_sign_out_button_click
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
        self.textbox_email_login = forms.TextBox()
        # password
        label_pw_login = forms.Label(Text='Password:')
        self.passwordbox_pw_login = forms.PasswordBox()
        # login button
        self.LoginButton = forms.Button(Text='Sign in')
        self.LoginButton.Click += self.on_login_button_click
        # add to layout
        grouplayout_login.AddRow(label_email_login, self.textbox_email_login)
        grouplayout_login.AddRow(label_pw_login, self.passwordbox_pw_login)
        grouplayout_login.AddRow(None, self.LoginButton)
        self.m_groupbox_login.Content = grouplayout_login

        # Signup Groupbox
        self.m_groupbox_signup = forms.GroupBox(Text='Sign up new account')
        self.m_groupbox_signup.Padding = drawing.Padding(5)
        # layout
        grouplayout_signup = forms.DynamicLayout()
        grouplayout_signup.Spacing = drawing.Size(200, 20)
        # name
        label_name_signup = forms.Label(Text='Name:')
        self.textbox_name_signup = forms.TextBox()
        # email
        label_email_signup = forms.Label(Text='Email:')
        self.textbox_email_signup = forms.TextBox()
        # password
        label_pw_signup = forms.Label(Text='Password:')
        self.passwordbox_pw_signup = forms.PasswordBox()
        # password repeat
        label_pwrp_signup = forms.Label(Text='Repeat password:')
        self.passwordbox_pwrp_signup = forms.PasswordBox()
        # signup button
        self.signupButton = forms.Button(Text='Sign up')
        self.signupButton.Click += self.on_signup_button_click
        # add to layout
        grouplayout_signup.AddRow(label_name_signup, self.textbox_name_signup)
        grouplayout_signup.AddRow(
            label_email_signup, self.textbox_email_signup)
        grouplayout_signup.AddRow(label_pw_signup, self.passwordbox_pw_signup)
        grouplayout_signup.AddRow(
            label_pwrp_signup, self.passwordbox_pwrp_signup)
        grouplayout_signup.AddRow(None, self.signupButton)
        self.m_groupbox_signup.Content = grouplayout_signup

        # Create the abort button
        self.AbortButton = forms.Button(Text='Cancel')
        self.AbortButton.Click += self.on_close_button_click

        # Create a table layout and add all the controls
        layout = forms.DynamicLayout()
        layout.Spacing = drawing.Size(200, 20)
        layout.AddRow(self.m_groupbox_status)
        layout.AddRow(self.m_groupbox_login)
        layout.AddRow(self.m_groupbox_signup)
        layout.AddRow(None)  # spacer
        layout.AddRow(self.AbortButton)

        # Set the dialog content
        self.Content = layout

    # Get the value of the textbox

    def get_text_login(self):
        return {
            'email': self.textbox_email_login.Text,
            'password': self.passwordbox_pw_login.Text
        }

    def get_text_signup(self):
        return {
            'name': self.textbox_name_signup.Text,
            'email': self.textbox_email_signup.Text,
            'password': self.passwordbox_pw_signup.Text,
            'password2': self.passwordbox_pwrp_signup.Text
        }

    # Close button click handler
    def on_close_button_click(self, sender, e):
        self.Close(False)

    # OK button click handler
    def on_login_button_click(self, sender, e):
        if self.textbox_email_login.Text == "" or self.passwordbox_pw_login.Text == "":
            raise Exception("Please provide credentials")
        else:
            self.Close(True)

    def on_signup_button_click(self, sender, e):
        if self.textbox_name_signup.Text == "" or self.textbox_email_signup.Text == "" or self.passwordbox_pw_signup.Text == "" or self.passwordbox_pwrp_signup.Text == "":
            raise Exception("Please provide credentials")
        else:
            data = self.get_text_signup()
            if data['password'] == data['password2']:
                api.signup(name=data['name'], email=data['email'], password=data['password'])
                user = models.User(email=data['email'])
                user.user_login(password=data['password'])
            else:
                raise Exception("Passwords are not matching")
            self.Close(True)

    # signout
    def on_sign_out_button_click(self, sender, e):
        api.logout()
        self.Close(True)

    @staticmethod
    def get_login_status():
        return api.check_login_status()['is_logged']


def request_account():
    dialog = AccountInfo()
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow)
    if (rc):
        return dialog.get_text_login()


def RunCommand(is_interactive):
    credentials = request_account()
    if not credentials:
        return 0
    if credentials['email'] and credentials['password']:
        user = models.User(email=credentials['email'])
        user.user_login(password=credentials['password'])


if __name__ == "__main__":
    RunCommand(True)
