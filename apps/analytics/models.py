#!/usr/bin/env python

import logging
import random

from google.appengine.api   import memcache
from google.appengine.ext   import db

from util.consts            import URL
from util.helpers           import generate_uuid

NUM_CLICK_SHARDS = 5

