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

def to_dict(something, recursion=0):
    import datetime
    import time
    output = {}

    SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)
    if recursion > 3:
        logging.error('recursion too much, returning: %s' % str(something))
        return str(something)

    for key, prop in something.properties().iteritems():
        value = getattr(something, key)
        logging.error('processing: %s' % key)

        try:
            if value is None or isinstance(value, SIMPLE_TYPES):
                output[key] = value
            elif isinstance(value, datetime.date) or \
                    isinstance(value, datetime.datetime):
                # Convert date/datetime to ms-since-epoch ("new Date()").
                ms = time.mktime(value.utctimetuple()) * 1000
                ms += getattr(value, 'microseconds', 0) / 1000
                output[key] = int(ms)
            elif isinstance(value, db.GeoPt):
                output[key] = {'lat': value.lat, 'lon': value.lon}
            elif isinstance(value, db.Model):
                output[key] = to_dict(value, recursion=recursion+1)
            else:
                output[key] = str(value)
                logging.error('weird value: %s' % str(value))
                #raise ValueError('cannot encode ' + repr(prop))
        except Exception, e:
            logging.error(e, exc_info=True)
    return output

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
            name = 'appsy_user_uuid', 
            value = user_uuid,
            expires_days= 365*10,
            domain = '.%s' % APP_DOMAIN)

def read_user_cookie( request_handler ):
    """Sets a cookie to identify a user"""
    cookieutil = LilCookies(request_handler, COOKIE_SECRET)
    user_uuid = cookieutil.get_secure_cookie(name = 'appsy_user_uuid')
    logging.info("Reading a user cookie: %s" % user_uuid)
    return user_uuid

def getURIForView(l, index, value):
    """ gets index of value in tuple"""
    for pos,t in enumerate(l):
        if t[index].__name__ == value:
            return pos

    # Matches behavior of list.index
    raise ValueError("list.index(x): x not in list")

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

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
