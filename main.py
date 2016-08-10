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

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def escape_html(s):
    return cgi.escape(s, quote = True)

def valid_month(month):
    month1 = month.capitalize()
    if month1 in months:
        return month1
    else:
        return None

def valid_day(day):
    if(type(day)==str and day.isdigit()):
        day = int(day)
        if(day<32 and day>0):
            return day
    elif(type(day)==int and day<32 and day>0):
        return day
    else:
        return None

def valid_year(year):
    if(type(year)==str and year.isdigit() and int(year)<2021 and int(year)>1899):
        return int(year)
    elif(type(year)==int and year<2021 and year>1899):
        return year
    else:
        return None

form="""
<form>
    What is your birthdate?
    <br>
    <label>
        Month
        <input type="text" name="month" value="%(month)s">
    </label>
    <label>
        Day
        <input type="text" name="day" value="%(day)s">
    </label>
    <label>
        Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""

class MainHandler(webapp2.RequestHandler):

    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": escape_html(month),
                                        "day": escape_html(day),
                                        "year": escape_html(year)})

    def get(self):
        self.write_form()

class TestHandler(webapp2.RequestHandler):
    def post(self):
        user_month=self.request.get('month')
        user_day=self.request.get('day')
        user_year=self.request.get('year')

        month=valid_month(user_month)
        day=valid_day(user_day)
        year=valid_year(user_year)

        if not(month and day and year):
            self.write_form("That's not true, my friend!", user_month, user_day, user_year)
        else:
            self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a valid input!")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks',ThanksHandler)
], debug=True)
