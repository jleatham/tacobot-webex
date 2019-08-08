import os
import sys
import random
import requests
import json
import urllib.request
from requests_toolbelt.multipart.encoder import MultipartEncoder


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
                 ['https://media.giphy.com/media/WNs0uptipSG40/giphy.gif',      'Everybody gets a Taco!'],
                 ['https://media.giphy.com/media/pYCdxGyLFSwgw/giphy.gif',      "It's raining Tacos!"],
                 ['https://media.giphy.com/media/EHCNlAWDPcOME/giphy.gif',      'Taco Time!'],
                 ['https://i.gifer.com/2KJm.gif',  'Is it Taco day already?'],
                 ['https://media.giphy.com/media/kGK4VeSwqEfbW/giphy.gif',      'All meetings are better with Tacos'],
                 ['https://media.giphy.com/media/pxXV5nDJhHthm/giphy.gif',      "♫ Do you want to bring a Taco? ♫ ... ♫ It doesn't have to be a Taco ♫ "],
                 ['https://media.giphy.com/media/3o7ZeT4XKYLG6x8zqo/giphy.gif', 'Surround yourself with Tacos, not negativity.'],
                 ['https://media.giphy.com/media/3o7ZezGPktFNZj93os/giphy.gif', 'It is only Tacos all the way down'],
                 ['https://media.giphy.com/media/3o6ZsUk2bRRhmROuw8/giphy.gif', 'Everybody loves Tacos'],
                 ['https://i.gifer.com/310p.gif',"It's a great day for Tacos"],
                 ['https://i.gifer.com/4QNn.gif','You cannot make everybody happy, you are not a Taco.'],
                 ['https://i.gifer.com/MZ8.gif','Sergeant TacoBot, at your service'],
                 ['https://i.gifer.com/3W3.gif','¿Como se dice Taco en español?']
                ]

def bot_send_gif(room_id, gif, message):
    #try to post
    payload = {"roomId": room_id,
               "markdown": message,
               "files":[gif]}
    response = requests.request("POST", 'https://api.ciscospark.com/v1/messages', data=json.dumps(payload), headers=TACO_HEADERS)
    #error handling
    print(f"sending gif to {room_id}")
    if response.status_code != 200:
        #modify function to receive user_input as well so we can pass through
        #user_input = "some test message for the moment"
        #send to the DEVs bot room
        #error_handling(response,response.status_code,user_input,room_id,headers)
        print("error posting to room")

def bot_send_gif_v2(room_id, gif, message):
    #try to post
    m = MultipartEncoder({
                      'roomId': room_id,
                      'text': message,
                      'files': (gif, open(gif, 'rb'),
                      'image/gif')})
    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                    headers={'Authorization': os.environ['TACO_TOKEN'],
                    'Content-Type': m.content_type})
    return r.text


def NTX_TACO_SELECTOR(room_id):    
    random_dallas = random.choice(PROCESSED_EMAIL_LIST_DALLAS)
    random_austin = random.choice(PROCESSED_EMAIL_LIST_AUSTIN)
    random_taco_messsage = random.choice(TACO_MESSAGE)
    urllib.request.urlretrieve(random_taco_messsage[0], 'taco.gif')

    bot_send_gif_v2(room_id,'taco.gif', random_taco_messsage[1])
    bot_post_to_room(room_id,f"<@personEmail:{random_dallas}@cisco.com|{random_dallas}> and <@personEmail:{random_austin}@cisco.com|{random_austin}>:  You're on deck to bring Tacos tomorrow!",TACO_HEADERS)



def get_msg_sent_to_bot(msg_id, headers):
    urltext = URL + "/" + msg_id
    payload = ""

    response = requests.request("GET", urltext, data=payload, headers=headers)
    response = json.loads(response.text)
    #print ("Message to bot : {}".format(response["text"]))
    return response["text"]



def old_process_bot_input_command(room_id,command, headers, bot_name):
    """ 
        Give generic response for now if spoken to.
        Add a test command to run what it would look like
    """
    test_command_list = ['test']
    pause_command_list = ['stop','pause']
    possible_command_list = test_command_list + pause_command_list
    command_list = command.split(' ')
    event_trigger = list(set(command_list).intersection(possible_command_list))
    if event_trigger:
        '''
        #remove command trigger and keep what is left
        for i in event_trigger:
            command = command.replace(i,'').strip()
        '''
        if any(item in test_command_list for item in event_trigger):
            msg_list = []
            
            msg_list.append("Set to run every {} where 0 = Mon , 4 = Friday, etc \n\n".format(DAY_TO_RUN))
            msg_list.append("Names are chosen at random and currently are hardcoded to the NTX region, split by city \n\n")
            msg_list.append("Will be posted into hardcoded room id: NTX general \n\n")
            msg_list.append("**Example output of TacoBot :** \n\n\n\n")
            msg = ''.join(msg_list)
            response = bot_post_to_room(room_id, msg, headers)
            NTX_TACO_SELECTOR(room_id)
        elif any(item in pause_command_list  for item in event_trigger):
            msg_list = []
            
            msg_list.append("**No need to bring TACOs this week** \n\n")
            msg_list.append("You have angered the tacobot \n\n")
            msg = ''.join(msg_list)
            response = bot_post_to_room(room_id, msg, headers)            
    else:
        bot_post_to_room(room_id,"Only commands I know are: **TEST** , and **pause** .  All values hard-coded at the moment and messages sent on schedule.",TACO_HEADERS)




def process_bot_input_command(room_id,command, headers, bot_name):
    """ 
        Provides a few different command options based in different lists. (commands should be lower case)
        Combines all lists together and checks if any keyword commands are detected...basically a manually created case/switch statement
        For each possible command, do something
        Is there an easier way to do this?
    """
    #ss_client = ss_get_client(os.environ['SMARTSHEET_TOKEN'])
    #state_filter = []
    #arch_filter = []
    #mobile_filter = False
    #url_filter = False
    #data = []
    
    '''
        pause : when we don’t need tacos that week
        spin: when a respin is needed , for PTO, etc
        naughty : when someone forgets …(Nate)… this will anger the taco bot and will increase their chances of being picked for a month
        add/remove: have a database of names that can be modified (for extended team, etc)
        designate: manually assign someone for the week
        list the individuals in the list, their current probability of being picked, and how many times they have been picked, etc
    '''

    command_list = [
        ("test",['test','-t']),
        ("pause",['pause','-p']),
        ("spin",['spin','respin','redo','-s']),
        ("naughty",['naughty','bad','-n']),
        ("add",['add','-a']),
        ("remove",['remove','-r']),
        ("list",['list','-l'])
        #("command alias",["list of possible command entries"])
    ]
    result = command_parse(command_list,command)
    ##looks like: {"event":"TX FL AL","filter":"sec dc","mobile":""}
    if result:
        if "pause" in result:
            print(f"made it to pause:  {result['pause']}") 
            msg = (
                f"No need to bring TACOS this week \n\n""
                f"You have sadened the TACOBOT \n\n"
                #post sad tacobot gif/pic
            )
            response = bot_post_to_room(room_id, msg, headers)
        elif "spin" in result:
            print(f"made it to spin:  {result['spin']}") 
         
        elif "naughty" in result:
            print(f"made it to naughty:  {result['naughty']}") 

        elif "add" in result:
            print(f"made it to add:  {result['add']}") 

        elif "remove" in result:
            print(f"made it to remove:  {result['remove']}") 

        elif "list" in result:
            print(f"made it to list:  {result['list']}") 
        
        elif "test" in result:
            print(f"made it to test:  {result['test']}") 
            msg = (
                f"Set to run every {DAY_TO_RUN} where 0 = Mon , 4 = Friday, etc \n\n""
                f"Names are chosen at random and currently are hardcoded to the NTX region, split by city \n\n"
                f"Will be posted into hardcoded room id: NTX general \n\n"
                f"**Example output of TacoBot :** \n\n\n\n"
            )
            response = bot_post_to_room(room_id, msg, headers)
            NTX_TACO_SELECTOR(room_id)            
            '''
            msg_list.append("Set to run every {} where 0 = Mon , 4 = Friday, etc \n\n".format(DAY_TO_RUN))
            msg_list.append("Names are chosen at random and currently are hardcoded to the NTX region, split by city \n\n")
            msg_list.append("Will be posted into hardcoded room id: NTX general \n\n")
            msg_list.append("**Example output of TacoBot :** \n\n\n\n")
            msg = ''.join(msg_list)
            '''
        #data = get_all_data_and_filter(ss_client,EVENT_SMARTSHEET_ID, state_filter,arch_filter,url_filter,NO_COLUMN_FILTER)
        #communicate_to_user(ss_client,room_id,headers,bot_name,data,state_filter,arch_filter,mobile_filter,url_filter,help=False)
    else:
        #communicate_to_user(ss_client,room_id,headers,bot_name,data,state_filter,arch_filter,mobile_filter,url_filter,help=True)      




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

def command_parse(command_list,command):
    #potential problem: city name has event / events or mobile or phone in it.  Could search for space or beginning of string to filter that out.
    """
        Takes a command_list (list of tuples), as well as a command(string coming from webex)
        Takes the string and find values in between the commands associated with each command
        Returns a dict that contains each command found as a key, and the args/values associated
        {"event":"TX FL AL","filter":"sec dc","mobile":""}
    """
    result = {}
    combined_command_list = []
    for i in command_list:
        for x in i[1]:
            combined_command_list.append(x)

    for i in command_list:
        command_hash = list(set(combined_command_list).symmetric_difference(i[1]))
        start_search = "|".join(i[1])
        end_search = "|".join(command_hash) + "|$"
        #'(event|events|-e)(.*?)(-f|filter|-m|mobile)'
        #3 search groups in ()... interested in the second
        #when the command events is typed, regex will find event, strip the s, and put it as an arg...bug
        #I think that can be fixed by checking to make sure there is a space afterwards, but then what about
        #typing -m at the end of command, there won't be a space afterwards, and as this for loop progresses it
        #will place the -m at the start_search location. It won't detect it.  It will see the -m, it will see the 
        # end of string($), but it won't detect because the match because it would expect a -m_ with a space
        #I think I will just fix this in the sanitize command function by getting rid of single characters
        #
        #or i could just hard code a solution and strip S out of any result as I would never need it.  or likewise
        #just replace events with event before string goes through regex.
        search = re.findall(r'('+start_search+')(.*?)('+end_search+')', command)
        if search:

            result[i[0]] = sanitize_commands(search[0][1])
    return result

def sanitize_commands(string):
    """
        Could do a lot here but don't right now.  Here is a good article on it:
        https://www.kdnuggets.com/2018/03/text-data-preprocessing-walkthrough-python.html
    """
    string = string.replace('\xa0','') #an artifact from WebEx sometimes
    string = string.replace(',',' ') #replace commas with spaces
    string = ' '.join([w for w in string.split() if len(w)>1]) #remove all characters of length of 1
    return string
