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
            self.redirect( url( 'ShowPhonePage' ) )
            return

        # Otherwise, show a list of unregistered Users.
        users = User.all().filter( 'registration_state =', 'unregistered' )

        template_values = { 'users' : users }

        self.response.out.write(self.render_page('unregistered.html', template_values))

