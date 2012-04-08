#!/usr/bin/env python

from apps.stats.processes import *

urlpatterns = [
    (r'/stats.fetch',       FetchStats),
    
]
