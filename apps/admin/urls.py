#!/usr/bin/env python
from apps.admin.processes import *
from apps.admin.views     import *

urlpatterns = [
    # Views
    (r'/admin/makeUsers',        UserMaker),



]

