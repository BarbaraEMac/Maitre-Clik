#!/usr/bin/env python

#from apps.homepage.processes import *
from apps.homepage.views      import *

urlpatterns = [
    (r'/mobile(.*)',     ShowMobileApp), # Must be last
    (r'/()',             ShowDesktopPage) # Must be last
]
