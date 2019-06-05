from botFunctions import ROOM_TO_POST, DAY_TO_RUN, NTX_TACO_SELECTOR
from datetime import datetime



print(f"myScheduler.py running...current weekday == {datetime.now().weekday()}")
print(f"DAY_TO_RUN == {DAY_TO_RUN}")
print(f"ROOM_TO_POST == {ROOM_TO_POST}")
#heroku schedule to run every day at 8AM CST.  Only run this script on Thursday.
if str(datetime.now().weekday()) == DAY_TO_RUN: #0=Monday , 4=Friday, etc
    print("Made it past if statement")
    NTX_TACO_SELECTOR(ROOM_TO_POST)