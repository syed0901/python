import requests
import json


class PushBulletSendNotif:
    def __init__(self):
     pass
 
    def send_notification_via_pushbullet(self, title, body):
        data_send = {"type": "note", "title": title, "body": body}
     
        ACCESS_TOKEN = ''
        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                             headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Something wrong')

# Function
def init_push(title, body):
    w=PushBulletSendNotif()
    w.send_notification_via_pushbullet(title, body)  

# Main
if __name__ == '__main__':
    init_push(sys.argv[1], sys.argv[2])