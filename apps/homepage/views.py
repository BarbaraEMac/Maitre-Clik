#!/usr/bin/python
import logging

from google.appengine.api import memcache
from google.appengine.ext import webapp

from util.helpers    import url
from util.urihandler import URIHandler

class ShowMobileApp(URIHandler):
    def get(self, page):
        # Attempt to get a User. 
        user = self.get_user()

        # If no User, force them to register so we know who they are!
        if not user:
            self.redirect( url( 'ShowUnregisteredUser' ) )
            return

        template_values = { 'user' : user }
        
        logging.info(page)

        self.response.out.write(self.render_page('mobile/index.html', template_values))

class ShowDesktopPage(URIHandler):
    def get(self, page):
        template_values = { }
        
        self.response.out.write(self.render_page('index.html', template_values))

