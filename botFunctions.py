import os
import sys
import json
import requests
from myhug import TACO_HEADERS
from requests_toolbelt.multipart.encoder import MultipartEncoder


TACO_EMAIL = os.environ['TACO_EMAIL']
TACO_NAME = os.environ['TACO_NAME']
TACO_SMARTSHEET_ID = "---"
TEST_ROOM_ID = os.environ['TEST_ROOM_ID']
TEST_EMAIL_LIST_DALLAS = os.environ['TEST_EMAIL_LIST_DALLAS']
TEST_EMAIL_LIST_AUSTIN = os.environ['TEST_EMAIL_LIST_AUSTIN']
PROCESSED_EMAIL_LIST_DALLAS = TEST_EMAIL_LIST_DALLAS.split(' ')
PROCESSED_EMAIL_LIST_AUSTIN = TEST_EMAIL_LIST_AUSTIN.split(' ')

def bot_send_gif(room_id, gif):
    #try to post
    payload = {"roomId": room_id,
               "markdown": "Taco Time!",
               "files":[gif]}
    response = requests.request("POST", 'https://api.ciscospark.com/v1/messages', data=json.dumps(payload), headers=TACO_HEADERS)
    #error handling
    if response.status_code != 200:
        #modify function to receive user_input as well so we can pass through
        #user_input = "some test message for the moment"
        #send to the DEVs bot room
        #error_handling(response,response.status_code,user_input,room_id,headers)
        print("error posting to room")
