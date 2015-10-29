#!/usr/bin/env python
#
# Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
# This code may only be used under the BSD style license found at http://polymer.github.io/LICENSE.txt
# The complete set of authors may be found at http://polymer.github.io/AUTHORS.txt
# The complete set of contributors may be found at http://polymer.github.io/CONTRIBUTORS.txt
# Code distributed by Google as part of the polymer project is also
# subject to an additional IP rights grant found at http://polymer.github.io/PATENTS.txt

__author__ = 'e.bidelman@google.com (Eric Bidelman)'

import random
import time
import urllib
import urllib2


class Analytics(object):

  BASE_URL = 'https://www.google-analytics.com/collect/__utm.gif'

  def __init__(self, tracking_code, app_name, av):
    if not tracking_code:
      raise Exception('No tracking code was given')
    if not av:
      raise Exception('No application version was given')

    self.tracking_code = tracking_code
    self.av = av
    self.app_name = app_name
    self.client_id = '%s%s' % (time.time(), random.random())

  def send(self, path='/', recorded_at=None):
    """Sends one pageview entry to Google Analytics.
    This method constructs the appropriate URL and makes a GET request to the
    tracking API.
    Args:
      path: A string representing the url path of the pageview to record.
          URL query parameters may be included. The format should map to the
          the command that was issued:
            yeoman init -> /init
            yeoman add model -> /add/model
      recorded_at: When the hit was recorded in seconds since the epoch.
          If absent, now is used.
    Returns:
      True if message was sent, otherwise false.
    """
    recorded_at = recorded_at or time.time()

    params = {
      'v': '1', # GA API tracking version.
      'tid': self.tracking_code, # Tracking code ID.
      't': 'pageview', # Event type
      'cid': self.client_id, # Client ID
      'aip': '1', # Anonymize IP
      'qt': int((time.time() - recorded_at) * 1e3), # Queue Time. Delta (milliseconds) between now and when hit was recorded.
      'dp': path,
      'an': self.app_name, # Application Name.
      'av': self.av, # Application Version.
      'z': time.time() # Cache bust. Probably don't need, but be safe. Should be last param.
    }

    encoded_params = urllib.urlencode(params)

    url = '%s?%s' % (self.BASE_URL, encoded_params)

    try:
      response = urllib2.urlopen(url)
      if response.code == 200:
        return True
    except urllib2.URLError:
      return False

    return False
