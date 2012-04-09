#!/usr/bin/python

import logging

from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.helpers           import generate_uuid
from util.model             import Model

# ------------------------------------------------------------------------------
# Checkin Class Definition -----------------------------------------------------
# ------------------------------------------------------------------------------
class Checkin( Model ):
    """ The Checkin Class
        Denotes a Checkin for a Meal from a User.
        Properties:
            meal - The Meal that this Checkin is associated with. 
            user - The User who placed this Checkin.
    """
    
    uuid    = db.StringProperty( indexed=True )
    created = db.DateTimeProperty( auto_now_add=True, indexed=False )
    
    # The Meal that this Checkin is associated with.
    meal = db.ReferenceProperty( db.Model, collection_name='meal_checkins', indexed=True ) 
    
    # The User who checked-in.
    user = db.ReferenceProperty( db.Model, collection_name='user_checkins', indexed=True ) 
 
    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(Checkin, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datastore retrieval using memcache_key"""
        return db.Query(Checkin).filter('uuid =', uuid).get()
    
    @staticmethod
    def create( meal, user ):
        """ Constructor for Checkin class. 
            Input: meal & user should be Obj refs
            Output: returns the new Checkin obj.
        """
        
        uuid = generate_uuid( 10 )

        # Only 1 Checkin per {user, meal} allowed!
        if Checkin.get_by_user_and_meal( user, meal ) is None:
            checkin = Checkin( key_name = uuid,
                               uuid     = uuid,
                               meal     = meal,
                               user     = user )
            checkin.put()
            return checkin

        return None

    @staticmethod
    def get_by_user_and_meal( user, meal ):
        """ Given a user and a meal, return the corresponding Checkin.
            If none exist, None is returned.
        """
        return Checkin.all().filter( 'meal =', meal ).filter( 'user =', user ).get()
