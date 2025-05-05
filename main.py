import time
import datetime
import requests
import os

# Telegram bot config
TOKEN = os.environ['TOKEN']
CHAT_ID = os.environ['CHAT_ID']
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

# 防止重複發送
last_alert_sent = False

def send_alert(message):
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(API_URL, data=data)

def check_market_condition():
    # TODO: 改為真實股市條件
    return False, ""

def is_market_open():
    """Check if current time is during market hours"""
    now = datetime.datetime.now()
    start_time = datetime.time(9, 0)  # 9:00 AM
    end_time = datetime.time(13, 30)  # 1:30 PM
    return start_time <= now.time() <= end_time

while True:
    try:
        if is_market_open():
            condition, msg = check_market_condition()
            if condition and not last_alert_sent:
                send_alert(msg)
                last_alert_sent = True
        else:
            last_alert_sent = False  # Reset alert flag after market closes
        time.sleep(60)  # Check every minute while market is open
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
