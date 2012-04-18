#!/usr/bin/env python

import logging
from django.utils import simplejson as json

from apps.user.models       import User

from util.consts            import URL
from util.helpers           import set_user_cookie  
from util.helpers           import url
from util.urihandler        import URIHandler

class CreateUser( URIHandler ):
    def post( self ):
        first_name  = self.request.get( 'firstName' )
        last_name   = self.request.get( 'lastName' )
        email       = self.request.get( 'email' )
        
        user        = User.create( first_name, last_name, email )

        # Cache the User
        self.db_user = user

        # Have to do this here to avoid a circular reference
        set_user_cookie( self, user.uuid )
        
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write( json.dumps( { 'uuid' : user.uuid,
                                               'img'  : user.img } ) )

