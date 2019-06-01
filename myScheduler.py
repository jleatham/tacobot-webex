from myhug import TACO_HEADERS, bot_post_to_room, URL
from botFunctions import TEST_ROOM_ID, PROCESSED_EMAIL_LIST_DALLAS, PROCESSED_EMAIL_LIST_AUSTIN
from datetime import datetime
import random
import requests
import json

#chron runs every day at 8AM, so this needs to check if it is Thursday, and only run then.
print("hello test scheduler")

TACO_GIF_LIST = ['https://media.giphy.com/media/WNs0uptipSG40/giphy.gif',
            'https://media.giphy.com/media/pYCdxGyLFSwgw/giphy.gif',
            'https://media.giphy.com/media/EHCNlAWDPcOME/giphy.gif',
            'https://media.giphy.com/media/26tnlYdWMzIYdaocU/giphy.gif',
            'https://media.giphy.com/media/kGK4VeSwqEfbW/giphy.gif',
            'https://media.giphy.com/media/pxXV5nDJhHthm/giphy.gif',
            'https://media.giphy.com/media/3o7ZeT4XKYLG6x8zqo/giphy.gif',
            'https://media.giphy.com/media/3o7ZezGPktFNZj93os/giphy.gif',
            'https://media.giphy.com/media/3o6ZtkmiFtpBvii6uQ/giphy.gif']

TACO_MESSAGE = ['Taco Time!',
                'All meetings are better with Tacos',
                "♫ Frozen ♫  -- ♫ Do you want to bring a Taco? ♫ ... ♫ It doesn't have to be a Taco ♫ ",
                'You cannot make everybody happy, you are not a Taco.',
                'Surround yourself with Tacos, not negativity.',
                'Everybody loves Tacos']

def bot_send_gif(room_id, gif, message):
    #try to post
    payload = {"roomId": room_id,
               "markdown": message,
               "files":[gif]}
    response = requests.request("POST", 'https://api.ciscospark.com/v1/messages', data=json.dumps(payload), headers=TACO_HEADERS)
    #error handling
    if response.status_code != 200:
        #modify function to receive user_input as well so we can pass through
        #user_input = "some test message for the moment"
        #send to the DEVs bot room
        #error_handling(response,response.status_code,user_input,room_id,headers)
        print("error posting to room")


#heroku schedule to run every day at 8AM CST.  Only run this script on Thursday.
if datetime.now().weekday() == 4: #0=Monday , 4=Friday, etc
    random_dallas = random.choice(PROCESSED_EMAIL_LIST_DALLAS)
    random_austin = random.choice(PROCESSED_EMAIL_LIST_AUSTIN)
    random_taco_gif = random.choice(TACO_GIF_LIST)
    random_taco_messsage = random.choice(TACO_MESSAGE)


    bot_post_to_room(TEST_ROOM_ID,f"<@personEmail:jleatham@cisco.com|{random_dallas}> and <@personEmail:jleatham@cisco.com|{random_austin}>:  You're on deck to bring Tacos!",TACO_HEADERS)
    bot_send_gif(TEST_ROOM_ID,random_taco_gif, random_taco_messsage)
