#!/usr/bin/python
import logging

from google.appengine.api import memcache
from google.appengine.ext import webapp

from apps.user.models import User

from util.helpers    import url
from util.urihandler import URIHandler

class ShowMobileApp(URIHandler):
    def get(self, page):
        template_values = {  }
        
        # Attempt to get a User. 
        user = self.get_user()

        # If no User, force them to register so we know who they are!
        if not user:
            template_values.update( self.unregistered_users_view() )

        else:
            template_values.update( self.vote_view( user ) )

        self.response.out.write(self.render_page('mobile/index.html', template_values))

    def unregistered_users_view( self ):
        logging.info('Unregistered')
        # Otherwise, show a list of unregistered Users.
        new_values = { 'unregistered_users' : User.get_unregistered(),
                       'ShowUnregisteredUserView' : 1 }
                        
        return new_values

    def vote_view( self, user ):
        # Otherwise, show a list of unregistered Users.
        new_values = { 'user' : user,
                       'ShowVoteView' : 1 }
                        
        return new_values

class ShowDesktopPage(URIHandler):
    def get(self, page):
        template_values = { }
        
        self.response.out.write(self.render_page('index.html', template_values))
