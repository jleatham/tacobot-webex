from myhug import TACO_HEADERS, bot_post_to_room, URL
from botFunctions import TEST_ROOM_ID, PROCESSED_EMAIL_LIST_DALLAS, PROCESSED_EMAIL_LIST_AUSTIN
import random
import requests
import json
print("hello test scheduler")

random_dallas = random.choice(PROCESSED_EMAIL_LIST_DALLAS)
random_austin = random.choice(PROCESSED_EMAIL_LIST_AUSTIN)

bot_post_to_room(TEST_ROOM_ID,f"<@personEmail:jleatham@cisco.com|{random_dallas}>:  Taco Time! ",TACO_HEADERS)

