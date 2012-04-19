#!/usr/bin/python

import logging

from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.helpers           import generate_uuid
from util.model             import Model

# ------------------------------------------------------------------------------
# Meal Class Definition ------------------------------------------------
# ------------------------------------------------------------------------------
class Meal( Model ):
    """ The Meal Class
        Denotes a Meal of the "Maitre 'Clik" app.
    """
    
    uuid   = db.StringProperty      ( indexed = True )
    
    # A day timestamp (no time)
    date   = db.DateProperty        ( indexed = False, auto_now_add = True )
    
    # Either 'LUNCH' or 'DINNER'
    type   = db.CategoryProperty    ( indexed = False )

    # String of the menu for this list.
    menu   = db.StringProperty      ( indexed = False )

    # List of items in the meal. Used to pull out contextual meal data in the future.
    items  = db.StringListProperty  ( indexed = False )

    # Flag to grab the current meal quickly from the DB.
    # Will either hold "current_meal" or "past_meal" 
    status = db.StringProperty      ( indexed = True, default='current_meal' )

    # Voter's rating for this meal; in range [0, 100]
    rating = db.IntegerProperty     ( indexed = True, default=0 )

    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(Meal, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datastore retrieval using memcache_key"""
        return db.Query(Meal).filter('uuid =', uuid).get()
    
    @staticmethod
    def create( type, menu ):
        """ Constructor for Meal class. 
            Input: 
            Output: returns the new Meal obj.
        """
        
        uuid = generate_uuid( 10 )

        meal = Meal( key_name = uuid,
                     uuid     = uuid,
                     type     = type,
                     menu     = menu,
                     items    = menu.split(' ') )
        meal.put()
        return meal

    @staticmethod
    def get_current( ):
        return Meal.all().filter( 'status =', 'current_meal' ).get()

