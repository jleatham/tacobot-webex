from botFunctions import ROOM_TO_POST, DAY_TO_RUN, NTX_TACO_SELECTOR
from datetime import datetime



print("hello test scheduler")
#heroku schedule to run every day at 8AM CST.  Only run this script on Thursday.
if datetime.now().weekday() == DAY_TO_RUN: #0=Monday , 4=Friday, etc
    NTX_TACO_SELECTOR(ROOM_TO_POST)