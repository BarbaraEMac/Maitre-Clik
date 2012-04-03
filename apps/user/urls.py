#!/usr/bin/env python

from apps.user.processes import *
from apps.user.views     import *

urlpatterns = [
    # Views
    (r'/user/newuser',             ShowNewUser),
    (r'/user/unregistered',        ShowUnregisteredUser),

    # Processes
    (r'/user/create/(.*)',         CreateUser),
    (r'/user/register/(.*)',       RegisterUser),
    
]
