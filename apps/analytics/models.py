#!/usr/bin/env python

import logging
import random

from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.consts            import URL
from util.helpers           import generate_uuid

NUM_CLICK_SHARDS = 5


# TODO: put class in here

    def get_clicks_count(self):
        """Count this apps sharded clicks"""
        total = memcache.get(self.uuid+"AnalyticsClickCounter")
        if total is None:
            total = 0
            for counter in AnalyticsClickCounter.all().\
            filter('app_uuid =', self.uuid).fetch(NUM_CLICK_SHARDS):
                total += counter.count
            memcache.add(key=self.uuid+"AnalyticsClickCounter", value=total)
        return total
    
    def add_clicks(self, num):
        """add num clicks to this App's click counter"""
        def txn():
            index = random.randint(0, NUM_CLICK_SHARDS-1)
            shard_name = self.uuid + str(index)
            counter = AnalyticsClickCounter.get_by_key_name(shard_name)
            if counter is None:
                counter = AnalyticsClickCounter( key_name = shard_name, 
                                                 uuid     = self.uuid )
            counter.count += num
            counter.put()

        db.run_in_transaction(txn)
        memcache.incr(self.uuid+"AnalyticsClickCounter")

    def increment_clicks(self):
        """Increment this link's click counter"""
        self.add_clicks(1)

    def clear_clicks( self ):
        memcache.add(key=self.uuid+"AnalyticsClickCounter", value=0)

        for i in range( 0, NUM_CLICK_SHARDS ):
            shard_name = self.uuid + str(i)
            counter = AnalyticsClickCounter.get_by_key_name(shard_name)
            if counter:
                counter.count = 0;
                counter.put()

## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
class AnalyticsClickCounter(db.Model):
    """Sharded counter for clicks"""

    uuid = db.StringProperty (indexed=True, required=True)
    count          = db.IntegerProperty(indexed=False, required=True, default=0)





