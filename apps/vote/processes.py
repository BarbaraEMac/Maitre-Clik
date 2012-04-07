#!/usr/bin/env python

import logging

from urlparse               import urlparse

from apps.meal.models       import Meal
from apps.vote.models       import Vote

from util.consts            import *
from util.urihandler        import URIHandler

class DoVote( URIHandler ):
    def post( self ):
        user = self.get_user()

        vote = Vote.create( Meal.get_current(), 
                            user, 
                            int(self.request.get('value')) )

