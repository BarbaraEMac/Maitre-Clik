#!/usr/bin/python

from google.appengine.api import memcache
from google.appengine.ext import webapp

from util.urihandler import URIHandler

class ShowLandingPage(URIHandler):
    def get(self, page):
        template_values = { }
        
        self.response.out.write(self.render_page('landing.html', template_values))

