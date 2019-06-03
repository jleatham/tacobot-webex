import os
import sys
from datetime import datetime
import random
import requests
import json


TACO_EMAIL = os.environ['TACO_EMAIL']
TACO_NAME = os.environ['TACO_NAME']
TACO_SMARTSHEET_ID = "---"
DAY_TO_RUN = os.environ['DAY_TO_RUN']
ROOM_TO_POST = os.environ['ROOM_TO_POST']
TEST_ROOM_ID = os.environ['TEST_ROOM_ID']
TEST_EMAIL_LIST_DALLAS = os.environ['TEST_EMAIL_LIST_DALLAS']
TEST_EMAIL_LIST_AUSTIN = os.environ['TEST_EMAIL_LIST_AUSTIN']
PROCESSED_EMAIL_LIST_DALLAS = TEST_EMAIL_LIST_DALLAS.split(' ')
PROCESSED_EMAIL_LIST_AUSTIN = TEST_EMAIL_LIST_AUSTIN.split(' ')



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

def NTX_TACO_SELECTOR(room_id):    
    random_dallas = random.choice(PROCESSED_EMAIL_LIST_DALLAS)
    random_austin = random.choice(PROCESSED_EMAIL_LIST_AUSTIN)
    random_taco_gif = random.choice(TACO_GIF_LIST)
    random_taco_messsage = random.choice(TACO_MESSAGE)

    bot_post_to_room(room_id,f"<@personEmail:{random_dallas}@cisco.com|{random_dallas}> and <@personEmail:{random_austin}@cisco.com|{random_austin}>:  You're on deck to bring Tacos!",TACO_HEADERS)
    bot_send_gif(room_id,random_taco_gif, random_taco_messsage)



