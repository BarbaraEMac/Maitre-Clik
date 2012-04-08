#!/usr/bin/env python

from apps.user.processes import *
#from apps.user.views     import *

urlpatterns = [
    # Processes
    (r'/user/create',         CreateUser),
    (r'/user/register',       RegisterUser),
]
