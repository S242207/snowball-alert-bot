import os
import time
import requests

# Telegram config
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

def send_alert(msg):
    data = {'chat_id': CHAT_ID, 'text': msg}
    requests.post(API_URL, data=data)

def check_market_condition():
    # TODO: 改為實際條件
    return False, ""

while True:
    condition, msg = check_market_condition()
    if condition:
        send_alert(msg)
    time.sleep(300)
