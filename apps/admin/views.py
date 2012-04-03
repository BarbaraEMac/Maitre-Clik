#!/usr/bin/env python


from apps.user.models import User

from util.consts import *
from util.helpers import *
from util.urihandler import URIHandler 

class UserMaker( URIHandler ):
    def get( self ):
        return

        # Don't run this again!
        names = [ 'Yuriy Blokhin', 'Edward Livingston', 'Mike Roberts', 'Andrei Skarine', 'Chris Best', 'Chris Fairles', 'Daniel Hendry', 'Jonathan Meyer', 'Nick Belyaev',
        'Adam Allidina', 'Peter Heinke', 'Julian Haldenby', 'Michael MacKenzie', 'Angela Watkins', 'Peter Wagner', 'Vick Yao', 'Erika Podlovics', 'Christine Thayer', 'Heather Galt',
        'Adrian Kenny', 'Jairaj Sethi', 'Benjamin Chilibeck', 'Rob McLeod', 'Ted Livingston', 'Barbara Macdonald']
        
        urls = ['static/imgs/YuriyBlokhin.jpeg', 'static/imgs/EdwardLivingston.jpg', 'static/imgs/MichaelRoberts.jpg', 'static/imgs/AndreiSkarine.jpg', 'static/imgs/ChrisBest.jpg',
        'static/imgs/ChrisFairles.jpg', 'static/imgs/DanielHendry.jpg', 'static/imgs/JonathanMeyer.jpg', 'static/imgs/NikolayBelyaev.jpg', 'static/imgs/AdamAllidina.jpg',
        'static/imgs/PeterHeinke.jpg', 'static/imgs/JulianHaldenby.jpg', 'static/imgs/MichaelMacKenzie.jpg', 'static/imgs/AngelaWatkins.jpg', 'static/imgs/PeterWagner.jpg', 'static/imgs/VickYao.jpg', 'static/imgs/ErikaPodlovics.jpg', 'static/imgs/ChristineThayer.jpg', 'static/imgs/HeatherGalt.jpg', 'static/imgs/AdrianKenny.jpeg', 'static/imgs/JairajSethi.jpeg', 'static/imgs/BenjaminChilibeck.jpg', 'static/imgs/RobMcLeod.jpg', 'static/imgs/TedLivingston.jpg', 'static/imgs/BarbaraMacdonald.jpg']
        
        for i in range( 0, 25 ):
            user = User.create( names[i], urls[i] )

