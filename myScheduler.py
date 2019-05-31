from myhug import TACO_HEADERS, bot_post_to_room, URL
from botFunctions import TEST_ROOM_ID, PROCESSED_EMAIL_LIST_DALLAS, PROCESSED_EMAIL_LIST_AUSTIN
import random
print("hello test scheduler")

random_dallas = random.choice(PROCESSED_EMAIL_LIST_DALLAS)
random_austin = random.choice(PROCESSED_EMAIL_LIST_AUSTIN)

bot_post_to_room(TEST_ROOM_ID,f"{random_dallas}:  Taco Time! ",TACO_HEADERS)

def bot_post_to_person(person_email, message, headers):
    #try to post
    payload = {"toPersonEmail": person_email,"markdown": message}
    response = requests.request("POST", URL, data=json.dumps(payload), headers=headers)
    #error handling
    if response.status_code != 200:
        #modify function to receive user_input as well so we can pass through
        #user_input = "some test message for the moment"
        #send to the DEVs bot room
        #error_handling(response,response.status_code,user_input,room_id,headers)
        print("error posting to person")

bot_post_to_person('jleatham@cisco.com',"heyoh, it works", TACO_HEADERS)