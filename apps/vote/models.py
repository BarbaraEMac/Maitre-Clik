#!/usr/bin/python

import logging

from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.helpers           import generate_uuid
from util.model             import Model

# ------------------------------------------------------------------------------
# Vote Class Definition --------------------------------------------------------
# ------------------------------------------------------------------------------
class Vote( Model ):
    """ The Vote Class
        Denotes a Vote (Yes or No) for a Meal from a User.
        Properties:
            meal - The Meal that this Vote is associated with. 
            user - The User who placed this Vote.
            value - In range [1, 10], with 10 = best, 1 = worst
    """
    
    uuid    = db.StringProperty( indexed = True )
    created = db.DateTimeProperty( auto_now_add=True, indexed=False )
    
    # The Meal that this Vote is associated with.
    meal = db.ReferenceProperty(db.Model, collection_name='meal_votes', indexed=True) 
    
    # The User who placed this Vote.
    user = db.ReferenceProperty(db.Model, collection_name='user_votes', indexed=True) 

    # In range [1, 10], with 10 = best, 1 = worst
    value = db.IntegerProperty( indexed=False )
    
    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(Vote, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datastore retrieval using memcache_key"""
        return db.Query(Vote).filter('uuid =', uuid).get()
    
    @staticmethod
    def create( meal, user, val ):
        """ Constructor for Vote class. 
            Input: meal & user should be Obj refs & value should be an int
            Output: returns the new Vote obj.
        """
        
        uuid = generate_uuid( 10 )

        # Error check the val. it must be in range [1, 10]
        if val < 1:
            val = 1
        elif val > 10:
            val = 10

        # Only 1 Vote per {user, meal} allowed!
        if Vote.get_by_user_and_meal( user, meal ) is None:
            
            vote = Vote( key_name = uuid,
                         uuid     = uuid,
                         meal     = meal,
                         user     = user,
                         value    = val )
            vote.put()
        return vote

    @staticmethod
    def get_by_user_and_meal( user, meal ):
        return Vote.all().filter('meal =', meal).filter('user =', user).get()
