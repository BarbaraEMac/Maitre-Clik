#!/usr/bin/python

import logging

from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.helpers           import generate_uuid
from util.model             import Model

# ------------------------------------------------------------------------------
# Stats Class Definition --------------------------------------------------------
# ------------------------------------------------------------------------------
class Stats( Model ):
    """ The Stats Class
        Properties:
    """
    
    uuid    = db.StringProperty( indexed = True )
    
    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(Stats, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datastore retrieval using memcache_key"""
        return db.Query(Stats).filter('uuid =', uuid).get()
    
    @staticmethod
    def create( ):
        """ Constructor for Stats class. 
            Input: 
            Output: returns the new Stats obj.
        """
        
        uuid = generate_uuid( 10 )

        stats = Stats( key_name = uuid,
                      uuid     = uuid,
                    )
        stats.put()
        return stats
