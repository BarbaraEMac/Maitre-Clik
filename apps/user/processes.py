#!/usr/bin/env python

import logging

from apps.user.models       import User

from util.consts            import URL
from util.helpers           import set_user_cookie  
from util.helpers           import url
from util.urihandler        import URIHandler

class RegisterUser( URIHandler ):
    def get( self, uuid ):
        user = User.get( uuid )

        # Cache the User
        self.db_user = user

        # Register the User
        user.register()

        # Have to do this here to avoid a circular reference
        set_user_cookie( self, uuid )

        # Return back to main app!
        self.redirect( url( 'ShowMobileApp', '/user/%s' % uuid ) )
        
class CreateUser( URIHandler ):
    def post( self, name ):
        user = User.create( name, 'as' )

        # Cache the User
        self.db_user = user

        # Register the User
        user.register()

        # Have to do this here to avoid a circular reference
        set_user_cookie( self, uuid )

        # Return back to main app!
        self.redirect( url( 'ShowMobileApp', '/user/%s' % uuid ) )

