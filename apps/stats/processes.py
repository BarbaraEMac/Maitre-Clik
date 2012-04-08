#!/usr/bin/env python

import logging
from django.utils import simplejson as json
from urlparse               import urlparse

from util.consts            import *
from util.urihandler        import URIHandler

class FetchStats( URIHandler ):
    def get( self ):
       
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write( json.dumps( { } ) ) 
