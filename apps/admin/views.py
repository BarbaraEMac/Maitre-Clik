#!/usr/bin/env python


from apps.user.models import User

from util.consts import *
from util.helpers import *
from util.urihandler import URIHandler 

class UserMaker( URIHandler ):
    def get( self ):
        for i in range(0, 5):
            user = User.create( '%s_%d' % ('name', i), 'http://images.pictureshunt.com/pics/l/little_sloth-8828.jpg' )

