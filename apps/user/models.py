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
        Properties:
            name - a string of 'first last' names
            img  - a url to an image of the User
            state - either 'unregistered' or 'registered'
    """
    
    uuid    = db.StringProperty( indexed = True )
    created = db.DateTimeProperty( auto_now_add = True, indexed=False )
    
    name = db.StringProperty( indexed = False )
    img  = db.StringProperty( indexed = False )

    registration_state = db.StringProperty( default = 'unregistered', indexed = True )

    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(User, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datastore retrieval using memcache_key"""
        return db.Query(User).filter('uuid =', uuid).get()
    
    @staticmethod
    def create( name, img ):
        """ Constructor for User class. 
            Input: name & img should both be strings.
            Output: returns the new User obj.
        """
        
        uuid = generate_uuid( 10 )

        user = User( key_name = "%s_%s" % (name, uuid),
                     uuid     = uuid,
                     name     = name, 
                     img      = img )
        user.put()
        return user
