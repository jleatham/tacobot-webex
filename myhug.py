import hug
import os
import requests
import json
import re
from datetime import datetime
from botFunctions import TACO_EMAIL,TACO_NAME,TACO_SMARTSHEET_ID


URL = "https://api.ciscospark.com/v1/messages"

TACO_HEADERS = {
    'Authorization': os.environ['TACO_TOKEN'],
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}



@hug.post('/taco', examples='taco')
def taco(body):
    """
        Test bot for new features.
    """
    print("GOT {}: {}".format(type(body), repr(body)))
    room_id = body["data"]["roomId"]
    identity = body["data"]["personEmail"]
    text = body["data"]["id"]
    print("see POST from {}".format(identity))
    if identity != TACO_EMAIL:
        print("{}-----{}".format(identity,TACO_EMAIL))
        command = get_msg_sent_to_bot(text).lower()
        command = get_msg_sent_to_bot(text, TACO_HEADERS)
        command = (command.replace(TACO_NAME, '')).strip()
        command = (command.replace('@', '')).strip()
        print("stripped command: {}".format(command))
        #test_process_bot_input_command(room_id,command, TACO_HEADERS, TACO_NAME)
        #send_log_to_ss(TACO_NAME,str(datetime.now()),identity,command,room_id)
