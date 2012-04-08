#!/usr/bin/env python

import logging

from apps.checkin.models    import Checkin
from apps.meal.models       import Meal

from util.urihandler        import URIHandler

class CreateCheckin( URIHandler ):
    def post( self ):
        # Given a User uuid, create a Checkin obj. 
        user = User.get( self.request.get('user_uuid') )
        meal = Meal.get_current()

        Checkin.create( meal, user )
