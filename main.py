#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re


def build_page(content):
    page_header = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Signup Form</title>
            <style type="text/css"> 
                .error {color: red;}
            </style>
        </head>
    <body>  """

    # html boilerplate for the bottom of every page
    page_footer = """
        </body>
    </html> """
    
    return page_header + content + page_footer 


# global escape function
def escapeHtml(input):
    return cgi.escape(input, quote=True)


# regular expressions
USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USERNAME_REGEX.match(username)


PASSWORD_REGEX = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_REGEX.match(password)


EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s.]+$")
def valid_email(email):
    return not email or EMAIL_REGEX.match(email)


# Signup form
class MainHandler(webapp2.RequestHandler):
    def get(self):        
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        username = ""
        email = ""

        form_signup = """
        <h1>
                <a href="/">Signup Form</a>
        </h1>
        <form method="post">
            <table>
                <tr>
                    <td><label>Username</label></td>
                    <td>
                        <input name="username" type="text" value="%s" />
                        <span class="error">%s</span>
                    </td>
                </tr>
                <tr>
                    <td><label>Password</label></td>
                    <td>
                        <input name="password" type="password" />
                        <span class="error">%s</span>
                    </td>
                </tr>
                <tr>
                    <td><label>Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" />
                        <span class="error">%s</span>
                    </td>
                </tr>
                <tr>
                    <td><label>Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%s"/>
                        <span class="error">%s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form> 
        """% (username, error_username, error_password, error_verify, email, error_email)

        content = form_signup 
        self.response.write(build_page(content))


    def post(self):
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        username = ""
        email = ""

        have_error = False
        username = escapeHtml(self.request.get("username"))
        password = escapeHtml(self.request.get("password"))
        verify = escapeHtml(self.request.get("verify"))
        email = escapeHtml(self.request.get("email"))

        

        if not valid_username(username):
            error_username = "Usernames must be betweet 3-20 characters long, and contain only letters and numbers"
            have_error = True

        if not valid_password(password):
            error_password = "Passwords must be betweet 3-20 characters long"
            have_error = True

        if verify != password:
            error_verify = "Passwords must match"
            have_error = True

        if not valid_email(email):
            error_email = "Please enter a valid email"
            have_error = True

        if have_error == True:    
            form_signup = """
            <h1>
                <a href="/">Signup Form</a>
            </h1>
            <form method="post">
                <table>
                    <tr>
                      <td><label>Username</label></td>
                      <td>
                        <input name="username" type="text" value="%s" />
                        <span class="error">%s</span>
                     </td>
                  </tr>
                  <tr>
                    <td><label>Password</label></td>
                    <td>
                        <input name="password" type="password" />
                        <span class="error">%s</span>
                    </td>
                  </tr>
                  <tr>
                    <td><label>Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" />
                        <span class="error">%s</span>
                    </td>
                  </tr>
                  <tr>
                    <td><label>Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%s"/>
                        <span class="error">%s</span>
                    </td>
                  </tr>
              </table>
            <input type="submit">
          </form> 
          """% (username, error_username, error_password, error_verify, email, error_email)
            
            content = form_signup

            self.response.write(build_page(content))

        else:
            username_welcome = username
            self.redirect("/welcome?username=%s" % username_welcome)


# Welcome page for after succesful signup
class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username_welcome = self.request.get("username")
        escaped_username = escapeHtml(username_welcome)

        content = """
            <head>
                <title>Welcome Page</title>
            </head>
            <body>
                <h1>
                    Welcome, """ + escaped_username + """!                
                </h1> 
            """
        
        self.response.write(build_page(content))
    

app = webapp2.WSGIApplication([
    ('/', MainHandler), 
    ('/welcome', WelcomeHandler),
    ], debug=True)
