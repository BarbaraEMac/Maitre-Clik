#!/usr/bin/env python

import logging

from apps.checkin.models    import Checkin
from apps.meal.models       import Meal

from util.urihandler        import URIHandler

class CreateCheckin( URIHandler ):
    def post( self ):
        # Given a User uuid, create a Checkin obj. 
        user = User.get( self.request.get('user_uuid') )

        # Make sure this User hasn't checked in for this meal!
        meal = Meal.get_current()
        checkin = Checkin.get_by_user_and_meal( user, meal )

        if checkin is None:
            Checkin.create( meal, user )
