# Aeshtetic twitter bot

# uses data scraped from the body building website, bodybuilding.com

# picks a random muscle group
# generates a random title
# generates a markov model to produce 4 unique steps 
# tweets status as an image overlayed with instructions, with muscle groups and hashtags

import bb_markov as bbm
from math import ceil
import textwrap
from PIL import Image, ImageDraw, ImageFont
import tweepy, time, sys
import random

# generate workout

for i in range(1):
    random_chosen_muscle = bbm.generate_new_muscle_group()

    bbm.generate_specific_model(random_chosen_muscle)
    name = 'EotD: ' + bbm.get_exercise_name()
    muscle = 'Muscles Worked: ' + bbm.get_current_muscle()
    s1 = '1) ' + bbm.give_me_step1()
    s2 = '2) ' + bbm.give_me_step2()
    s3 = '3) ' + bbm.give_me_step3()
    s4 = '4) ' + bbm.give_me_step4()


    s1w = textwrap.wrap(s1,width=75)
    s2w = textwrap.wrap(s2,width=75)
    s3w = textwrap.wrap(s3,width=75)
    s4w = textwrap.wrap(s4,width=75)


    # prepare image
    # get an image
    base = Image.open(r'C:\Users\Charl\Dropbox\Python scripts\twitterbot\laptop\building-muscle.jpg').convert('RGBA')

    # make a blank image for the text, initialized to transparent text color
    txt = Image.new('RGBA', base.size, (255,255,255,0))

    # get a font
    fnt = ImageFont.truetype('C:/Windows/Fonts/Californian FB/CALIFR.TTF',20)
    # get a drawing context
    d = ImageDraw.Draw(txt)


    print len(s1w)
    print len(s2w)
    print len(s3w)
    print len(s4w)

    total_message = [name,muscle]
    total_message += s1w
    total_message += s2w
    total_message += s3w
    total_message += s4w

    total_lines = 2 + len(s1w) + len(s2w) + len(s3w) + len(s4w)

    x_pos = 10
    y_pos = 10
    inc = 25
    for i in range(total_lines):
        print "d.text(%d,%d)"%(x_pos,y_pos+inc*i)
        print total_message[i]
        d.text((x_pos,y_pos+inc*i),total_message[i],font=fnt, fill=(255,255,255,160))
        
    out = Image.alpha_composite(base, txt)
    out.save("test.jpg")

#exit()
    # TWEET THE FINAL PRODUCT

    #enter the corresponding information from your Twitter application:
    CONSUMER_KEY = 'CON_KEY'#keep the quotes, replace this with your consumer key
    CONSUMER_SECRET = 'CON_SEC'#keep the quotes, replace this with your consumer secret key
    ACCESS_KEY = 'ACC_KEY'#keep the quotes, replace this with your access token
    ACCESS_SECRET = 'ACC_SEC'#keep the quotes, replace this with your access token secret
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
     

    #tweet the picture and message with some hashtags
    status_message = total_message[0] + ' #workout #fitness #wotd #eotd' + ' #'+bbm.get_current_muscle()
    api.update_with_media('test.jpg',status=status_message)
    #time.sleep(60*5)
##
