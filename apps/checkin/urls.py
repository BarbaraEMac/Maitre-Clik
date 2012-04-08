#!/usr/bin/env python

from apps.checkin.processes import *
#from apps.user.views     import *

urlpatterns = [
    (r'/checkin/create',    CreateCheckin),
]
