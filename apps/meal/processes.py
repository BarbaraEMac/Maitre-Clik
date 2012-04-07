#!/usr/bin/env python

import logging

from urlparse               import urlparse

from apps.meal.models       import Meal
from util.consts            import *
from util.urihandler        import URIHandler

class LunchGenerator( URIHandler ):
    def get(self):
        # Update the current meal to become an old meal
        current_meal = Meal.get_current()
        current_meal.status = 'past_meal'
        current_meal.put()

        # Create the new meal
        new_meal = Meal.create( 'LUNCH', "" )

        # Sanity check
        if current_meal.meal != 'DINNER':
            logging.error("Meals are screwed up -> old:%s new: %s" % (current_meal.uuid, new_meal.uuid))

class DinnerGenerator( URIHandler ):
    def get(self):
        # Update the current meal to become an old meal
        current_meal = Meal.get_current()
        current_meal.status = 'past_meal'
        current_meal.put()

        # Create the new meal
        new_meal = Meal.create( 'DINNER', "" )
        
        # Sanity check
        if current_meal.meal != 'LUNCH':
            logging.error("Meals are screwed up -> old:%s new: %s" % (current_meal.uuid, new_meal.uuid))
