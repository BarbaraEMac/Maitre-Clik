#!/usr/bin/env python

import logging

from apps.meal.models       import Meal

from util.consts            import *
from util.urihandler        import URIHandler

class CreateMeal( URIHandler ):
    def post( self ):
        items = self.request.get('meal_items').strip()

        if items is not "":
            # Update the current meal to become an old meal
            type = 'DINNER'

            current_meal = Meal.get_current()
            if current_meal:
                current_meal.status = 'past_meal'
                current_meal.put()

                if current_meal.type == "LUNCH":
                    type = "DINNER"
                else:
                    type = "LUNCH"

            # Create the new meal
            new_meal = Meal.create( type, items )


class LunchGenerator( URIHandler ):
    def get(self):
        # Update the current meal to become an old meal
        current_meal = Meal.get_current()
        current_meal.status = 'past_meal'
        current_meal.put()

        # Create the new meal
        new_meal = Meal.create( 'LUNCH', "" )

        # Sanity check
        if current_meal.type != 'DINNER':
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
        if current_meal.type != 'LUNCH':
            logging.error("Meals are screwed up -> old:%s new: %s" % (current_meal.uuid, new_meal.uuid))
