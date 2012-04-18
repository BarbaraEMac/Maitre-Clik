#!/usr/bin/env python

from apps.meal.processes import *
from apps.meal.views     import *

urlpatterns = [

    (r'/meal/create',    CreateMeal)
    
]
