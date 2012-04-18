#!/usr/bin/env python
import logging

from google.appengine.api import mail
from google.appengine.api.mail import EmailMessage

###################
#### Addresses ####
###################

from_addr = '"Barbara" <z4beth@gmail.com>'

#####################
#### Email Class ####
#####################
class Email():
    
    @staticmethod
    def meal_notification( to_addr, first_name, menu ):
        # To be dispatched when a meal arrives.

        subject = "[Hungry?] Food's Here!"
        
        body = "<html> <head> <style> html { background-color: #c1e2f1; font-family: Helvetica; text-align: left; } #error { color: red; } #menu { margin-bottom: 30px; padding: 20px; border-radius: 5px; background-color: #BCE072; -moz-box-shadow: inset 0 0 10px #000000; -webkit-box-shadow: inset 0 0 10px #000000; box-shadow: inset 0 0 10px #000000; } </style> </head> <body> <p>Hi %s,</p> <p>Your delicious food has arrived. You'll be eating:</p> <p id='menu'>%s</p> <p id='error'>Don't forget to Clik-In before you eat!</p> <p>Enjoy!</p> </body> </html>" % ("name", "menu")
        
        Email.send_email( from_addr, to_addr, subject, body )


#####################################
#####################################
#####################################

    @staticmethod
    def send_email( from_addr, to_addr, subject, body ):
        e = EmailMessage(sender=from_addr, to=to_addr, subject=subject, html=body)
        e.send()

