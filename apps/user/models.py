#!/usr/bin/python

import hashlib
import logging

from django.utils           import simplejson as json
from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.consts            import *
from util.helpers           import generate_uuid
from util.model             import Model

# ------------------------------------------------------------------------------
# User Class Definition ------------------------------------------------
# ------------------------------------------------------------------------------
class User( Model ):
    """A User"""
    uuid    = db.StringProperty(indexed = True)
    created = db.DateTimeProperty(auto_now_add = True, indexed=False)
    
    # Owner Properties
    full_name = db.StringProperty( indexed = False )
    email     = db.StringProperty( indexed = True )

    def __init__(self, *args, **kwargs):
        self._memcache_key = kwargs['uuid'] if 'uuid' in kwargs else None 
        super(User, self).__init__(*args, **kwargs)
    
    @staticmethod
    def _get_from_datastore( uuid ):
        """Datauser retrieval using memcache_key"""
        return db.Query(User).filter('uuid =', uuid).get()
    
