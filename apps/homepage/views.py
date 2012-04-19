#!/usr/bin/python
import logging

from google.appengine.api import memcache
from google.appengine.ext import webapp

from apps.meal.models import Meal
from apps.user.models import User

from util.helpers     import url
from util.urihandler  import URIHandler

class ShowMobileApp(URIHandler):
    def get(self, page):
        template_values = {  }
        
        # Attempt to get a User. 
        user = self.get_user()

        # If no User, force them to register so we know who they are!
        if not user:
            template_values.update( { 'ShowOnboardView' : 1 } )

        else:
            template_values.update( { 'user'         : user,
                                      'ShowVoteView' : 1 } )

        self.response.out.write(self.render_page('mobile/index.html', template_values))

class ShowDesktopPage(URIHandler):
    def get(self, page):
        template_values = { 'meal' : Meal.get_current() }
        
        self.response.out.write(self.render_page('index.html', template_values))
