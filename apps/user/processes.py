#!/usr/bin/env python

import logging

from util.consts            import URL
from util.helpers           import set_user_cookie  
from util.helpers           import url
from util.urihandler        import URIHandler

class RegisterUser( URIHandler ):
    def get( self ):
        set_user_cookie( self, self.request.get( 'uuid' ) )
        
        self.redirect( url( 'ShowPhonePage' ) )
        
