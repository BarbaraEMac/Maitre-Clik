#!/usr/bin/python

# consts.py
# constants for Maitre Clik

import os
import logging

from urlparse import urlunsplit

# Domain Stuff
USING_DEV_SERVER    = True if 'Development' in os.environ.get('SERVER_SOFTWARE', "") else False
PROTOCOL            = 'http' 
SECURE_PROTOCOL     = 'https'
APP_DOMAIN          = 'None' if USING_DEV_SERVER else 'clik-app.appspot.com'
DOMAIN              = os.environ['HTTP_HOST'] if USING_DEV_SERVER else APP_DOMAIN 
URL                 = urlunsplit((PROTOCOL, DOMAIN, '', '', '')) 
SECURE_URL          = urlunsplit((SECURE_PROTOCOL, DOMAIN, '', '', '')) 
KEYS                = os.environ['HTTP_HOST']

# A BS P3P Header - thanks IE
P3P_HEADER = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'

# LilCookies (secure cookies) Stuff
COOKIE_SECRET = 'f54eb793d727492e99601446aa9b06bab504c3d37bc54c8391f385f0dde03732'

# number of seconds to memcache an item
# see: http://stackoverflow.com/questions/2793366/what-is-the-maximum-length-in-seconds-to-store-a-value-in-memcache
# TODO: Try 2591999 instead
MEMCACHE_TIMEOUT = 1728000

# List of root template directories
# to import templates from
TEMPLATE_DIRS = (
    'apps/homepage/templates',        
)

# the apps we are using
INSTALLED_APPS = [
    'admin',
    'analytics',
    'checkin',
    'homepage',
    'meal',
    'stats',
    'user',
    'vote'
]
