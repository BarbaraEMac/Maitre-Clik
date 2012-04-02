#!/usr/bin/env python

from apps.user.processes import *
from apps.user.views     import *

urlpatterns = [
    # Views
    (r'/user/unregistered',        ShowUnregisteredUser),

    # Processes
    (r'/user/register/(.*)',       RegisterUser),
    
]
