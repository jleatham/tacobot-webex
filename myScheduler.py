from myhug import TACO_HEADERS, bot_post_to_room, URL
from botFunctions import TEST_ROOM_ID
print("hello test scheduler")


bot_post_to_room(TEST_ROOM_ID,'test message',TACO_HEADERS)
