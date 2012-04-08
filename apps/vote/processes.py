#!/usr/bin/env python

import logging

from apps.meal.models       import Meal
from apps.vote.models       import Vote

from util.consts            import *
from util.urihandler        import URIHandler

class DoVote( URIHandler ):
    def post( self ):
        """ Let's a User assign a [1, 10] value for the current Meal. """
        user = self.get_user()
        meal = Meal.get_current()
        
        # Create the Vote.
        vote = Vote.create( meal, user, int(self.request.get('value') ) )

