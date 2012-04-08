#!/usr/bin/env python

import logging
from django.utils import simplejson as json

from apps.user.models       import User

from util.consts            import URL
from util.helpers           import set_user_cookie  
from util.helpers           import url
from util.urihandler        import URIHandler

class RegisterUser( URIHandler ):
    def post( self ):
        user = User.get( self.request.get( 'user_uuid') )
        
        # Cache the User
        self.db_user = user

        # Register the User
        user.register()

        # Have to do this here to avoid a circular reference
        set_user_cookie( self, user.uuid )

        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write( json.dumps( { 'name' : user.name, 
                                               'uuid' : user.uuid } ) )

class CreateUser( URIHandler ):
    def post( self ):
        user = User.create( self.request.get( 'name' ) )

        # Cache the User
        self.db_user = user

        # Register the User
        user.register()

        # Have to do this here to avoid a circular reference
        set_user_cookie( self, user.uuid )

        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write( json.dumps( { 'name' : user.name, 
                                               'uuid' : user.uuid } ) )
