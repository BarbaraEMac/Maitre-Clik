#!/usr/bin/env python

#from apps.homepage.processes import *
from apps.homepage.views      import *

urlpatterns = [
    (r'/stats',          ShowStats),

    (r'/mobile(.*)',     ShowMobileApp), # Must be last
    (r'/()',             ShowDesktopPage) # Must be last
]
