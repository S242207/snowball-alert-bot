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
last_alert_time = None  # 初始化為 None，後續將會記錄上次發送的時間

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
            # 檢查是否有需要發送的警報，並且避免重複發送
            if condition and not last_alert_sent:
                send_alert(msg)
                last_alert_sent = True
                last_alert_time = datetime.datetime.now()  # 更新最後發送警報的時間
            elif not condition:
                last_alert_sent = False  # 如果條件不滿足，重置為可以發送警報
        else:
            last_alert_sent = False  # 若市場關閉，重置為可以發送警報

        time.sleep(60)  # 每分鐘檢查一次

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
