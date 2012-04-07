#!/usr/bin/env python

from apps.vote.processes import *

urlpatterns = [
    (r'/vote/createVote',       DoVote),
    
]
