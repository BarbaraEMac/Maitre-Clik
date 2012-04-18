#!/usr/bin/python

import logging

from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.helpers           import generate_uuid
from util.model             import Model

# ------------------------------------------------------------------------------
# User Class Definition ------------------------------------------------
# ------------------------------------------------------------------------------
class User( Model ):
    """ The User Class
        Denotes a User of the "Maitre 'Clik" app.
    """
    
    uuid    = db.StringProperty    ( indexed = True )
    created = db.DateTimeProperty  ( indexed = False, auto_now_add = True )
    
    # The User's first name
    first_name  = db.StringProperty( indexed = False )
    
    # The User's last name
    last_name   = db.StringProperty( indexed = False )
    
    # The User's email
    email       = db.StringProperty( indexed = True )
    
    # URL to an image of this User
    img         = db.StringProperty( indexed = False, default = '/static/imgs/DefaultProfile.jpg' )
    
    # True iff the User wants to receive an email when a meal arrives
    notification = db.BooleanProperty( indexed = True, default = True )

    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(User, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datastore retrieval using memcache_key"""
        return db.Query(User).filter('uuid =', uuid).get()
    
    @staticmethod
    def create( first_name, last_name, email ):
        """ Constructor for User class. 
            Input: name & img should both be strings.
            Output: returns the new User obj.
        """
        
        uuid = generate_uuid( 10 )

        # Santization lite lol
        first_name = first_name.strip()
        last_name  = last_name.strip()
        email      = email.strip()

        user = User( key_name     = "%s%s_%s" % (first_name, last_name, uuid),
                     uuid         = uuid,
                     first_name   = first_name,
                     last_name    = last_name,
                     email        = email,
                     notification = (email is not "") )
        user.put()
        return user

