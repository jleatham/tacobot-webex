import os
import sys
import json
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
