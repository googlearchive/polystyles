#!/usr/bin/env python
#
# Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
# This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
# The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
# The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
# Code distributed by Google as part of the polymer project is also
# subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt

__author__ = 'e.bidelman@google.com (Eric Bidelman)'

import re
import unittest
import urllib
import webapp2
import webtest

from google.appengine.api import memcache
from google.appengine.ext import testbed
from google.appengine.api import urlfetch

import handlers


class HandlerTest(unittest.TestCase):

  def setUp(self):
    app = webapp2.WSGIApplication([('/', handlers.MainHandler)])
    self.testapp = webtest.TestApp(app)
    self.testbed = testbed.Testbed()
    self.testbed.activate()

  def tearDown(self):
    self.testbed.deactivate()

  def testMainHandler(self):
    response = self.testapp.get('/')
    self.assertEqual(response.status_int, 200)
    self.assertEqual(response.content_type, 'text/html')
    self.assertEqual(
        response.headers['Access-Control-Allow-Origin'], '*', 'CORs enabled')

  def testStylesParam(self):
    styles = ':host{display:block;}'
    response = self.testapp.get('/?styles=' + urllib.quote(styles))
    self.assertEqual(response.status_int, 200)
    body = response.body.strip()
    result = re.search(styles, body)
    self.assertIsNotNone(result)

  def testURLParam(self):
    self.testbed.init_urlfetch_stub()
    self.testbed.init_memcache_stub()

    url = 'https://www.polymer-project.org/css/homepage.css'

    self.assertIsNone(memcache.get(url), 'url pre-fetch is not in memcache')

    actual_file = urlfetch.fetch(url)
    response = self.testapp.get('/?url=' + url)
    self.assertEqual(response.status_int, 200)
    self.assertIsNotNone(memcache.get(url), 'url post-fetch is in memcache')
    self.assertEqual(actual_file.content, memcache.get(url))

    body = response.body.strip()
    self.assertTrue(actual_file.content in body)

  def testIdParam(self):
    response = self.testapp.get('/?id=my-styles')
    self.assertEqual(response.status_int, 200)
    body = response.body.strip()
    result = re.match(r'^<dom-module id\="my-styles">', body)
    self.assertIsNotNone(result, 'custom id used')

  def testOnlyCSSFilesAllowed(self):
    self.testbed.init_urlfetch_stub()
    self.testbed.init_memcache_stub()

    url = 'https://www.polymer-project.org/1.0/docs/start/getting-the-code.html'
    actual_file = urlfetch.fetch(url)

    self.assertEqual(actual_file.status_code, 200)
    self.assertEqual(actual_file.headers['Content-Type'], 'text/html')

    response = self.testapp.get('/?url=' + url)
    self.assertEqual(response.status_int, 200)

    body = response.body.strip()
    self.assertFalse(actual_file.content in body)
    self.assertTrue(re.search('Error', body))

  def test404File(self):
    self.testbed.init_urlfetch_stub()
    self.testbed.init_memcache_stub()

    url = 'https://example.com/app.css'
    actual_file = urlfetch.fetch(url)

    self.assertEqual(actual_file.status_code, 404)

    response = self.testapp.get('/?url=' + url)
    self.assertEqual(response.status_int, 200)

    self.assertFalse(actual_file.content in response.body)
    self.assertTrue(re.search('Error', response.body))


if __name__ == '__main__':
  unittest.main()
