import os
import sys
import requests
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
    """
        Sends the email file generated using MultipartEncoder which
        breaks the requests into tiny peices to get past the 5K Teams limit

    """
    m = MultipartEncoder({'roomId': room_id,
                      'text': 'Taco Time!',
                      'files': (gif,gif,'image/gif')})
    r = requests.post('https://api.ciscospark.com/v1/messages', data=m,
                    headers={'Authorization': os.environ['TACO_TOKEN'],
                    'Content-Type': m.content_type})
    return r.text
