import time
import datetime
import requests
import os

# 初始化變數
last_alert_time = None  # 初始化 last_alert_time

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
    start_time = datetime.time(9, 0)  # 開盤時間 09:00
    end_time = datetime.time(13, 30)  # 收盤時間 13:30
    return start_time <= now.time() <= end_time

while True:
    try:
        if is_market_open():
            condition, msg = check_market_condition()
            if condition and not last_alert_sent:
                send_alert(msg)
                last_alert_sent = True
            else:
                last_alert_sent = False  # Reset after market closes
        time.sleep(60)  # 每分鐘檢查一次
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
