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



      

def build_page(textarea_content):
    page_header = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Signup Form</title>
            <style type="text/css"> 
                .error {color: red;}
            </style>
        </head>
    <body>
        <h1>
                <a href="/">Signup Form</a>
        </h1>  """

    # html boilerplate for the bottom of every page
    page_footer = """
        </body>
    </html> """

    # html signin form 
    form_signup = """
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form> """
    return page_header + form_signup + page_footer 

def build_welcome(textarea_content):
    page_header = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Welcome Page</title>
            <style type="text/css"> 
                .error {color: red;}
            </style>
        </head>
        <body>
            <h1>
                Welcome, {{username}}!                
            </h1> 
        </body>
    </html> """
    return page_header 

USERNAME_REGEX = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USERNAME_REGEX.match(username)


PASSWORD_REGEX = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_REGEX.match(password)


EMAIL_REGEX = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s.]+$")
def valid_email(email):
    return not email or EMAIL_REGEX.match(email)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        content = build_page("")
        self.response.write(content)

    
    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('werify')
        email = self.request.get('email')

        # this stores the username and email so we can return it if there is an error
        params = dict(username = username,
                      email = email)
       
       if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.response.write(content, **params)
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(Basehandler):
    def get(self):
        username = self.request.get('username'):
        if valid_username(username):
            self.response.write(content, username=username)
        else:
            self.response.write(build_welcome)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', Signup),
    ('/welcome', Welcome),
], debug=True)
