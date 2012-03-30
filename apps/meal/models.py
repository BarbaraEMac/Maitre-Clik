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
        Properties:
            date  - A day timestamp (no time)
            meal  - Either 'LUNCH' or 'DINNER'
            items - List of items in the meal. Used to pull out contextual meal data in the future.
    """
    
    uuid = db.StringProperty( indexed= True )
    
    # A day timestamp (no time)
    date = db.DateProperty( auto_now_add=True, indexed=False )
    
    # Either 'LUNCH' or 'DINNER'
    meal = db.CategoryProperty( indexed=False )

    # List of items in the meal. Used to pull out contextual meal data in the future.
    items = db.StringListProperty( indexed=False )

    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(Meal, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datastore retrieval using memcache_key"""
        return db.Query(Meal).filter('uuid =', uuid).get()
    
    @staticmethod
    def create( meal, items ):
        """ Constructor for Meal class. 
            Input: 
            Output: returns the new Meal obj.
        """
        
        uuid = generate_uuid( 10 )

        meal = Meal( key_name = uuid,
                     uuid     = uuid,
                     meal     = meal,
                     items    = items.split(',') )
        meal.put()
        return meal
