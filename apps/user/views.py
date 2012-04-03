#!/usr/bin/env python

import logging

from apps.user.models       import User

from util.consts            import URL
from util.helpers           import url
from util.urihandler        import URIHandler

class ShowUnregisteredUser( URIHandler ):
    def get( self ):
        # Assert that we don't have a User here
        user = self.get_user()

        # If we do, then redirect bakc to main app
        if user:
            self.redirect( url( 'ShowMobileApp', '/user/%s' % user.uuid ) )
            return

        k = User.get_unregistered()
        logging.info("Got %d %s" % (k.count(), k))
        
        # Otherwise, show a list of unregistered Users.
        template_values = { 'unregistered_users' : User.get_unregistered() }

        self.response.out.write(self.render_page('unregistered.html', template_values))


class ShowNewUser( URIHandler ):
    def get( self ):
        template_values = {  }

        self.response.out.write(self.render_page('newuser.html', template_values))

 

