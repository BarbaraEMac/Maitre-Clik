#!/usr/bin/env python

#from apps.homepage.processes import *
from apps.homepage.views      import *

urlpatterns = [

    (r'/()',             ShowLandingPage) # Must be last
]
