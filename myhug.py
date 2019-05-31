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
        command = get_msg_sent_to_bot(text, TACO_HEADERS)
        command = (command.replace(TACO_NAME, '')).strip()
        command = (command.replace('@', '')).strip()
        print("stripped command: {}".format(command))
        process_bot_input_command(room_id,command, TACO_HEADERS, TACO_NAME)
        #send_log_to_ss(TACO_NAME,str(datetime.now()),identity,command,room_id)



def get_msg_sent_to_bot(msg_id, headers):
    urltext = URL + "/" + msg_id
    payload = ""

    response = requests.request("GET", urltext, data=payload, headers=headers)
    response = json.loads(response.text)
    #print ("Message to bot : {}".format(response["text"]))
    return response["text"]



def bot_post_to_room(room_id, message, headers):
    #try to post
    payload = {"roomId": room_id,"markdown": message}
    response = requests.request("POST", URL, data=json.dumps(payload), headers=headers)
    #error handling
    if response.status_code != 200:
        #modify function to receive user_input as well so we can pass through
        #user_input = "some test message for the moment"
        #send to the DEVs bot room
        #error_handling(response,response.status_code,user_input,room_id,headers)
        print("error posting to room")
