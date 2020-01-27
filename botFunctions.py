import os
import sys
import random
import requests
import json
import urllib.request
from requests_toolbelt.multipart.encoder import MultipartEncoder
import re
import smartsheet
from datetime import datetime


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

SMARTSHEET_ID = os.environ['SMARTSHEET_ID']   #tacobot sheet
SMARTSHEET_TOKEN = os.environ['SMARTSHEET_TOKEN']


URL = "https://api.ciscospark.com/v1/messages"

TACO_HEADERS = {
    'Authorization': os.environ['TACO_TOKEN'],
    'Content-Type': "application/json",
    'cache-control': "no-cache"
}


def ss_get_client(SMARTSHEET_TOKEN):
    #ss_client = smartsheet.Smartsheet(os.environ['SMARTSHEET_TOKEN'])
    ss_client = smartsheet.Smartsheet(SMARTSHEET_TOKEN)
    # Make sure we don't miss any errors
    ss_client.errors_as_exceptions(True)
    return ss_client

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

RANDOM_RESPONSES = [ "Please don't encourage the TACOBOT",
                  "Every now and then I fall apart",
                  "Dinosaurs had no TACOs, how did that work out?",
                  "Do you want to TACO bout it?",
                  "Taco Love language 1 of 5: Words of Affirmation: Your Tacos are delicious!",
                  "Taco Love language 2 of 5: Acts of Service: I made you Tacos!",
                  "Taco Love language 3 of 5: Receiving Gifts: Here's a Taco!",
                  "Taco Love language 4 of 5: Quality Time: Let's go out for Tacos together!"
                  #"Taco Love language 5 of 5: Physical Touch: Let me hold you like a taco!"
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

def taco_selector():
    '''
        Get all people and their associated roomIDs and emails.  Will be a list of dicts for each row.  
        Create a new list where we combine all the individual rows that have the same room_id into a new dict : {'room_id': 'asdf','members':[['John','john@comp.com'],['Jane','jane@comp.com'],'[etc]'],'post_date':'etc'... }
    '''
    all_room_ids_list = []
    member_pick_list = []
    to_modify = []

    #get all Smart Sheet Data
       #dict of rows with the column as key    
    all_data_list = get_ss_data()
    #unpause any member if current date is greater than 'pause' date (add to-modify list)
    #get all roomIDs while looping then remove duplicates
    for row in all_data_list:
        if row["roomID"]: #helps sanitize the data for weird SS quirks
            all_room_ids_list.append(row["roomID"])
            if row["pause"]:
                if datetime.now() > datetime.strptime(row["pause"], '%Y-%m-%d'):
                    to_modify.append({"ss_row_id":row["ss_row_id"],"flag":"unpause"})
    all_room_ids_list = list(set(all_room_ids_list))

    #For each roomID
        #if default_create: get the runday/time
        #else add members to members field of dict

        #append to member_pick_list
    for room in all_room_ids_list:
        row_dict = {"members":[]}
        for row in all_data_list:
            if room == row["roomID"]:
                if row["name"] == "default_create":
                    if row["weekday_to_run"] == "Monday":
                        row_dict["weekday_to_run"] = "0"
                    elif row["weekday_to_run"] == "Tuesday":
                        row_dict["weekday_to_run"] = "1"   
                    elif row["weekday_to_run"] == "Wednesday":
                        row_dict["weekday_to_run"] = "2"    
                    elif row["weekday_to_run"] == "Thursday":
                        row_dict["weekday_to_run"] = "3"    
                    elif row["weekday_to_run"] == "Friday":
                        row_dict["weekday_to_run"] = "4"    
                    elif row["weekday_to_run"] == "Saturday":
                        row_dict["weekday_to_run"] = "5"    
                    elif row["weekday_to_run"] == "Sunday":
                        row_dict["weekday_to_run"] = "6"  

                    row_dict["run_period"] = row["run_period"]
                    row_dict["time_to_run"] = row["time_to_run"]
                    row_dict["roomID"] = row["roomID"]
                elif row["name"] and not row["pause"]:
                    row_dict["members"].append([row["name"],row["email"],row["select_count"],row["ss_row_id"]])
        member_pick_list.append(row_dict)
    

    #For each room, check if it is the correct day to run
    #then check if it is the correct hour to run
    #then check if the week of the month is correct

    #if yes to above, randomly select member in room
        #post to room
        #add selected member to to_modify list  
    for row in member_pick_list:
        if str(datetime.now().weekday()) == row["weekday_to_run"]: #0=Monday , 4=Friday, etc
            if int(datetime.now().hour) == int(float(row["time_to_run"])):
                
                day_of_month = datetime.now().day
                if (((day_of_month <= 7 ) and (row["run_period"] == "First of Month")) or
                    ((8 <= day_of_month <= 14) and (row["run_period"] == "Second of Month")) or
                    ((15 <= day_of_month <= 21) and (row["run_period"] == "Third of Month")) or
                    ((22 <= day_of_month <= 28) and (row["run_period"] == "Fourth of Month")) or
                    ((day_of_month <= 29) and (row["run_period"] == "Fifth of Month")) or
                    (row["run_period"] == "Every Week")):

                    print("Made it past if statement")
                    the_taco_giver = weighted_random_select(row["members"])
                    random_taco_messsage = random.choice(TACO_MESSAGE)
                    urllib.request.urlretrieve(random_taco_messsage[0], 'taco.gif')
                    response = bot_send_gif_v2(row["roomID"],'taco.gif', random_taco_messsage[1])
                    print(response)
                    bot_post_to_room(row["roomID"],f"<@personEmail:{the_taco_giver[1]}|{the_taco_giver[0]}> :  You're on deck to bring Tacos to the next meeting!",TACO_HEADERS)
                    print(f'{the_taco_giver[2]}')
                    try:
                        count = str(int(float(the_taco_giver[2]))+1)
                    except:
                        count = "1"
                    to_modify.append({"ss_row_id":the_taco_giver[3],"flag":"count","count":count})
    
    
    #modify smartsheet all at once
    for row in to_modify:
        modify_smart_sheet(row)

def get_ss_data():
    ss_client = ss_get_client(SMARTSHEET_TOKEN)
    sheet = ss_client.Sheets.get_sheet(SMARTSHEET_ID)
    all_data_list = []
    for row in sheet.rows:
        row_dict = {}
        row_dict["ss_row_id"] = str(row.id)
        #row_dict["url"] = ""        
        for cell in row.cells:
            #map the column id to the column name
            #map the cell data to the column or '' if null
            column_title = map_cell_data_to_columnId(sheet.columns, cell)
            if cell.value:
                row_dict[column_title] = str(cell.value)
            else:
                row_dict[column_title] = ''    
       
        all_data_list.append(row_dict)
    return all_data_list

def weighted_random_select(ptp_list):
    #ptp = Potential Taco Providers
    '''
        list of list is provided: [['name','email','1.0','123423423'],[...]]
        representing name,email,times selected,smartsheet row ID
        Goal is to identify the members(s) who have provided the least amount of tacos...
        And select them before anyone else.  If multiple have given the same, select randomly
        End result is a randomized round robin
    '''
    weight = []
    tacos_given = []
    for i in ptp_list:
        if not i[2]:
            l = 0
        else:
            l = int(float(i[2]))        
        tacos_given.append(l)
    limit = sorted(list(set(tacos_given)))[0]  #get unique numbers, sort them, only grab the first/lowest, these people need 
    #to be selected next
    for i in ptp_list:
        if not i[2]:
            l = 0
        else:
            l = int(float(i[2]))
        if l == limit:
            w = 1
            weight.append(w)
        else:
            weight.append(0)
            
    c = random.choices(
        population=ptp_list,
        weights=weight,
        k=1
    )    
    return c[0]

def map_cell_data_to_columnId(columns,cell):
    """
        helper function to map smartsheet column IDs to their name value without hardcoding
        pass in the parsed objects from smartsheet(the entire set of columns and the individual cell)
        then iterate until the ids match and return the associated column name
        could also make processing simpler by creating a card to fill out with who and when.
    """
    
    #cell object has listing for column_id , but data shows {columnId: n}, weird
    for column in columns:
        if column.id == cell.column_id:
            return column.title

def modify_smart_sheet(row):
    '''
        roomID : 3362571592984452
        name: 7866171220354948
        email: 2236671686141828
        birth_month: 6893064775067524
        birth_day: 1263565240854404
        pause: 6740271313512324
        select_count: 4488471499827076

    '''
    headers = {'Authorization': "Bearer "+SMARTSHEET_TOKEN,'Content-Type': "application/json"}
    if row["flag"] == "unpause": 
        url = f"https://api.smartsheet.com/2.0/sheets/{SMARTSHEET_ID}/rows/{row['ss_row_id']}"    
        payload = ( f'{{"id":{row["ss_row_id"]}, "cells": [ '
                    f'{{"columnId": 6740271313512324,  "value": "",    "strict": false}}'
                    f'] }}')     
        response = requests.put(url, data=payload, headers=headers)
        #print(response.content)
    if row["flag"] == "count":
        url = f"https://api.smartsheet.com/2.0/sheets/{SMARTSHEET_ID}/rows/{row['ss_row_id']}"    
        print(f"{url}")
        payload = ( f'{{"id":{row["ss_row_id"]}, "cells": [ '
                    f'{{"columnId": 4488471499827076,  "value": "{row["count"]}",    "strict": false}}'
                    f'] }}')     
        response = requests.put(url, data=payload, headers=headers)
        #print(response.content)
    if row["flag"] == "pause":
        url = f"https://api.smartsheet.com/2.0/sheets/{SMARTSHEET_ID}/rows/{row['ss_row_id']}"    
        payload = ( f'{{"id":{row["ss_row_id"]}, "cells": [ '
                    f'{{"columnId": 6740271313512324,  "value": "{row["pause"]}",    "strict": false}}'
                    f'] }}')     
        response = requests.put(url, data=payload, headers=headers)
        #print(response.content)


def get_msg_sent_to_bot(msg_id, headers):
    urltext = URL + "/" + msg_id
    payload = ""

    response = requests.request("GET", urltext, data=payload, headers=headers)
    response = json.loads(response.text)
    #print ("Message to bot : {}".format(response["text"]))
    return response["text"]


def pause_taco_bot(room_id,date=False,flag="room"):
    '''
        Take a room and a date and put pause on all the members (or maybe just the defalt_create member)
        or if the flag is for an individual, just pause them.
        If no date is given, just take the next meeting time, add by 1 interval, and minus a day/hour/etc
        so that it will run the following meeting
        Shouls probably take the taco_selector def and split it into multiple defs and reuse that code for
        this def.
    '''
    pass


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
        ("test",['-t']),
        ("pause",['pause','-p']),
        ("spin",['spin','respin','redo','-s']),
        ("naughty",['naughty','bad','-n','angry','forgot','lazy','trouble','slack']),
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
                f"No need to bring TACOS this week \n"
                f"You have sadened the TACOBOT \n\n"
                #post sad tacobot gif/pic
            )
            response = bot_post_to_room(room_id, msg, headers)
        elif "spin" in result:
            print(f"made it to spin:  {result['spin']}") 
         
        elif "naughty" in result:
            print(f"made it to naughty:  {result['naughty']}") 
            msg = (
                f"Shame! \n"
                f"You have angered the TACOBOT \n\n"
                #post angry tacobot gif/pic
            )
            response = bot_post_to_room(room_id, msg, headers)
        elif "add" in result:
            print(f"made it to add:  {result['add']}") 

        elif "remove" in result:
            print(f"made it to remove:  {result['remove']}") 

        elif "list" in result:
            print(f"made it to list:  {result['list']}") 
        
        elif "test" in result:
            print(f"made it to test:  {result['test']}") 
            msg = (
                f"Room ID = {room_id} \n"
                f"Set to run every {DAY_TO_RUN} where 0 = Mon , 4 = Friday, etc \n\n"
                f"Names are chosen at random and currently are hardcoded to the NTX region, split by city \n\n"
                f"Will be posted into hardcoded room id: NTX general \n\n"
                f"**Example output of TacoBot :** \n\n\n\n"
            )
            response = bot_post_to_room(room_id, msg, headers)
            #NTX_TACO_SELECTOR(room_id)     
            taco_selector()       

        #data = get_all_data_and_filter(ss_client,EVENT_SMARTSHEET_ID, state_filter,arch_filter,url_filter,NO_COLUMN_FILTER)
        #communicate_to_user(ss_client,room_id,headers,bot_name,data,state_filter,arch_filter,mobile_filter,url_filter,help=False)
    else:
        bot_post_to_room(room_id,random.choice(RANDOM_RESPONSES),TACO_HEADERS)
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
