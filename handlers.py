#!/usr/bin/env python
#
# Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
# This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
# The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
# The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
# Code distributed by Google as part of the polymer project is also
# subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt

__author__ = 'e.bidelman@google.com (Eric Bidelman)'

import os
import jinja2
import webapp2

from google.appengine.api import memcache
from google.appengine.api import urlfetch

import analytics


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

ga = analytics.Analytics('UA-39334307-14', 'Polymer PolyStyle', '0.0.1')

def fetch_stylesheet(url):
  styles = memcache.get(url)

  if styles is None:
    result = urlfetch.fetch(url, deadline=5)

    if result.status_code == 200:
      if result.headers['Content-Type'] == 'text/css':
        styles = result.content
        memcache.add(url, styles, time=3600) # cache for 1 hr.
      else:
        styles = '/* Error - only CSS filres are allowed %s */' % url
    else:
      styles = '/* Error %s - %s */' % (result.status_code, url)

  return styles


class MainHandler(webapp2.RequestHandler):

  def get(self):
    styles = self.request.get('styles', '')

     # Stylesheet urls takes precedence over styles.
    url = self.request.get('url', None)
    if url:
      styles = fetch_stylesheet(url)

    data = {
      'id': self.request.get('id', 'shared-styles'),
      'styles': styles
    }

    self.response.headers['Access-Control-Allow-Origin'] = '*'
    # self.response.headers['Content-Type'] = 'text/plain'

    template = JINJA_ENVIRONMENT.get_template('style_module_template.html')

    ga.send('/') # send pageview to GA.

    return self.response.write(template.render(data))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=False)
