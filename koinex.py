import time
import json
import requests
from notif import *
from time import sleep

URL = "https://koinex.in/api/ticker"


while True:
    koinex_data = json.loads(requests.get(URL).text)
    #print koinex_data
    xrp = koinex_data['prices']['XRP']
    w=WindowsBalloonTip()
    
    if xrp != "":
        w.handleNotif("Ripple Current value", xrp)
    time.sleep(600)