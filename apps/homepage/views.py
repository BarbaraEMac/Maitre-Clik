#!/usr/bin/python
import logging

from google.appengine.api import memcache
from google.appengine.ext import webapp

from util.urihandler import URIHandler

class ShowPhonePage(URIHandler):
    def get(self):
        template_values = { }
        
        self.response.out.write(self.render_page('mobile/index.html', template_values))

class ShowDesktopPage(URIHandler):
    def get(self, page):
        template_values = { }
        
        self.response.out.write(self.render_page('index.html', template_values))

