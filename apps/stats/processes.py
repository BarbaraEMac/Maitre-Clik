#!/usr/bin/env python

import logging
from django.utils       import simplejson as json

from apps.meal.models   import Meal
from apps.checkin.models import Checkin
from apps.stats.models  import Stats

from util.urihandler    import URIHandler

class FetchStats( URIHandler ):
    def get( self ):
       
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write( json.dumps( { } ) ) 

class CrawlLunch( URIHandler ):
    def post( self ):
        return self.get( )

    def get( self ):
        meal     = Meal.get_current()
        stats    = Stats.all().get()
        checkins = Checkin.get_by_meal( meal )
        
        stats.lunch_checkin_count += checkins.count()
        stats.lunch_checkin_days  += 1

        stats.put()

class CrawlDinner( URIHandler ):
    def post( self ):
        return self.get()
    def get( self ):
        return
