#!/usr/bin/python

import logging, os
import inspect

from google.appengine.ext        import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from apps.user.models   import User
from util.consts        import *
from util.helpers       import read_user_cookie
from util.helpers       import set_user_cookie
from util.templates     import render 

class URIHandler( webapp.RequestHandler ):

    def __init__(self):
        # For simple caching purposes. Do not directly access this. Use self.get_user() instead.
        try:
            self.response.headers.add_header('P3P', P3P_HEADER)
        except:
            pass
        self.db_user = None

    # Return None if not authenticated.
    # Otherwise return db instance of user.
    def get_user(self):
        if self.db_user:
            return self.db_user
        
        # Try to fetch a User via cookie
        self.db_user = User.get( read_user_cookie( self ) )

        return self.db_user
    
    def render_page(self, template_file_name, content_template_values, template_path=None):
        """This re-renders the full page with the specified template."""
        user = self.get_user()

        template_values = {
            'URL'  : URL,
            'user' : user
        }
        merged_values = dict(template_values)
        merged_values.update(content_template_values)
        
        path = os.path.join('templates/', template_file_name)
        
        app_path = self.get_app_path()

        if template_path != None:
            logging.info('got template_path: %s' % template_path)
            path = os.path.join(template_path, path)
        elif app_path != None:
            path = os.path.join(app_path, path)

        # Make sure the cookie is always set.
        if user:
            set_user_cookie( self, user.uuid )

        logging.info("Rendering %s" % path )
        self.response.headers.add_header('P3P', P3P_HEADER)
        return render(path, merged_values)

    def get_app_path(self):
        module = inspect.getmodule(self).__name__
        parts = module.split('.')
        app_path = None 
        
        if len(parts) > 2:
            if parts[0] == 'apps':
                # we have an app
                app_path = '/'.join(parts[:-1])

        return app_path

