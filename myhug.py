import hug
import os
import requests
import json
import re
from datetime import datetime
from botFunctions import URL, TACO_HEADERS,TACO_EMAIL,TACO_NAME,TACO_SMARTSHEET_ID, DAY_TO_RUN, NTX_TACO_SELECTOR 
from botFunctions import bot_post_to_room, get_msg_sent_to_bot, process_bot_input_command





@hug.post('/taco', examples='taco')
def taco(body):
    """
        Test bot for new features.
    """
    #print("GOT {}: {}".format(type(body), repr(body)))
    room_id = body["data"]["roomId"]
    identity = body["data"]["personEmail"]
    text = body["data"]["id"]
    #print("see POST from {}".format(identity))
    if identity != TACO_EMAIL:
        #print("{}-----{}".format(identity,TACO_EMAIL))
        command = get_msg_sent_to_bot(text, TACO_HEADERS)
        command = command.lower()
        command = (command.replace(TACO_NAME, '')).strip()
        command = (command.replace('@', '')).strip()
        print("stripped command: {}".format(command))
        process_bot_input_command(room_id,command, TACO_HEADERS, TACO_NAME)
        #send_log_to_ss(TACO_NAME,str(datetime.now()),identity,command,room_id)



