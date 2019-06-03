import os
import sys
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

URL = "https://api.ciscospark.com/v1/messages"

TACO_HEADERS = {
    'Authorization': os.environ['TACO_TOKEN'],
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}


TACO_MESSAGE = [
                 ['https://media.giphy.com/media/WNs0uptipSG40/giphy.gif',      'Everybody gets a TACO!'],
                 ['https://media.giphy.com/media/pYCdxGyLFSwgw/giphy.gif',      "It's raining Tacos!"],
                 ['https://media.giphy.com/media/EHCNlAWDPcOME/giphy.gif',      'Taco Time!'],
                 ['https://media.giphy.com/media/26tnlYdWMzIYdaocU/giphy.gif',  'You cannot make everybody happy, you are not a Taco.'],
                 ['https://media.giphy.com/media/kGK4VeSwqEfbW/giphy.gif',      'All meetings are better with Tacos'],
                 ['https://media.giphy.com/media/pxXV5nDJhHthm/giphy.gif',      "♫ Do you want to bring a Taco? ♫ ... ♫ It doesn't have to be a Taco ♫ "],
                 ['https://media.giphy.com/media/3o7ZeT4XKYLG6x8zqo/giphy.gif', 'Surround yourself with Tacos, not negativity.'],
                 ['https://media.giphy.com/media/3o7ZezGPktFNZj93os/giphy.gif', 'It is only Tacos all the way down'],
                 ['https://media.giphy.com/media/3o6ZtkmiFtpBvii6uQ/giphy.gif', 'Everybody loves Tacos']
                ]

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
    random_taco_messsage = random.choice(TACO_MESSAGE)

    bot_post_to_room(room_id,f"<@personEmail:{random_dallas}@cisco.com|{random_dallas}> and <@personEmail:{random_austin}@cisco.com|{random_austin}>:  You're on deck to bring Tacos!",TACO_HEADERS)
    bot_send_gif(room_id,random_taco_messsage[0], random_taco_messsage[1])



def get_msg_sent_to_bot(msg_id, headers):
    urltext = URL + "/" + msg_id
    payload = ""

    response = requests.request("GET", urltext, data=payload, headers=headers)
    response = json.loads(response.text)
    #print ("Message to bot : {}".format(response["text"]))
    return response["text"]



def process_bot_input_command(room_id,command, headers, bot_name):
    """ 
        Give generic response for now if spoken to.
        Add a test command to run what it would look like
    """
    possible_command_list = ['test','Test','TEST']
    command_list = command.split(' ')
    event_trigger = list(set(command_list).intersection(possible_command_list))
    if event_trigger:
        '''
        #remove command trigger and keep what is left
        for i in event_trigger:
            command = command.replace(i,'').strip()
        '''
        msg_list = []
        
        msg_list.append("Set to run every {} where 0 = Mon , 4 = Friday, etc \n\n".format(DAY_TO_RUN))
        msg_list.append("Names are chosen at random and currently are hardcoded to the NTX region, split by city \n\n")
        msg_list.append("Will be posted into hardcoded room id: NTX general \n\n")
        msg_list.append("**Example output of TacoBot :** \n\n\n\n")
        msg = ''.join(msg_list)
        response = bot_post_to_room(room_id, msg, headers)
        NTX_TACO_SELECTOR(room_id)
    else:
        bot_post_to_room(room_id,"Only command I know is: **TEST** .  All values hard-coded at the moment and messages sent on schedule.",TACO_HEADERS)




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

