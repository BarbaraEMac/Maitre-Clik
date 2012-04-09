#!/usr/bin/env python

import Cookie
import logging
import re
import urllib
import urllib2
import uuid

from google.appengine.ext import db
from google.appengine.ext import webapp

from util.consts  import *
from util.cookies import LilCookies

def generate_uuid( digits ):
    """Generate a 'digits'-character hex endcoded string as
    a random identifier, with collision detection"""
    while True:    
        tmp = min(digits, 32)
        uid = uuid.uuid4().hex[:tmp]
        digits -= 32
        if digits <= 32:
            break

    return uid

# Cookie Stuff
def set_user_cookie(request_handler, user_uuid):
    """Sets a cookie to identify a user"""
    logging.info("Setting a user cookie: %s" % user_uuid)
    cookieutil = LilCookies(request_handler, COOKIE_SECRET)
    cookieutil.set_secure_cookie(
            name = 'maitre_clik_user_uuid', 
            value = user_uuid,
            expires_days= 365*10,
            domain = '.%s' % APP_DOMAIN)

def read_user_cookie( request_handler ):
    """Sets a cookie to identify a user"""
    cookieutil = LilCookies(request_handler, COOKIE_SECRET)
    user_uuid = cookieutil.get_secure_cookie(name = 'maitre_clik_user_uuid')
    logging.info("Reading a user cookie: %s" % user_uuid)
    return user_uuid

def url(view, *args, **kwargs):
    """
    looks up a url for a view
        - view is a string, name of the view (such as ShowRoutes)
        - args are optional parameters for that view
        - **kwargs takes a named argument qs. qs is passed to
            urllib.urlencode and tacked on to the end of the url
            Basically, use this to pass a dict of arguments
        example usage: url('ShowDashboard', '12512512', qs={'order': 'date'})
            - this would return a url to the ShowDashboard view, for the
              dashboard id 12512512, and pass the order=date
            - /app/12512512/?order=date
        example: url('ShowProfilePage', '1252', '2151', qs={'format':'json'})
            - /user/1252/2151/?format=json
    """
    url = None
    try:
        app = webapp.WSGIApplication.active_instance
        handler = app.get_registered_handler_by_name(view)

        logging.info('handler: %s' % handler)

        url = handler.get_url(*args)

        qs = kwargs.get('qs', ())
        if qs:
            url += '?%s' % urllib.urlencode(qs)

        logging.info(qs)
        logging.info('got url: %s' % url)
    except:
        logging.warn('could not reverse url %s' % view)

    return url  

