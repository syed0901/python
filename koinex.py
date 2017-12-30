import time
import json
import requests
from notif import *
from pushNotif import *
from time import sleep

URL = "https://koinex.in/api/ticker"
title="Ripple Value"

while True:
    koinex_data = json.loads(requests.get(URL).text)
    #print koinex_data
    xrp = koinex_data['prices']['XRP']
    w=WindowsBalloonTip()
    p=PushBulletSendNotif()
    
    if xrp != "":
        w.handleNotif("Ripple Current value", xrp)
        p.send_notification_via_pushbullet(title,xrp)
    time.sleep(600)
