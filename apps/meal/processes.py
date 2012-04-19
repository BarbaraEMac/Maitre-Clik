#!/usr/bin/env python

import logging
from google.appengine.api   import taskqueue

from apps.meal.models       import Meal
from apps.user.models       import User

from util.consts            import *
from util.helpers           import url
from util.urihandler        import URIHandler

class CreateMeal( URIHandler ):
    def post( self ):
        menu   = self.request.get('menu').strip()
        type   = self.request.get('type').upper()
        rating = self.request.get('rating')

        if menu is not "":
            # Update the current meal to become an old meal
            current_meal = Meal.get_current()
            if current_meal:
                current_meal.status = 'past_meal'
                current_meal.rating = int( rating )
                current_meal.put()

            # Create the new meal
            new_meal = Meal.create( type, menu )

            # Tell people the meal is here!!!
            users = User.all().filter( 'notification =', True ).filter( 'email !=', '' )
            for u in users:
                taskqueue.add( queue_name = 'notificationEmail', 
                               url        = url( 'NotifyUsers' ),
                               params     = {'first_name' : u.first_name,
                                             'email'      : u.email,
                                             'menu'       : menu } )
