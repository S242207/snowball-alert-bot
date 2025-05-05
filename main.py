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
last_alert_time = None  # Initialize last_alert_time as None

def send_alert(message):
    """Function to send alert via Telegram bot"""
    try:
        data = {'chat_id': CHAT_ID, 'text': message}
        response = requests.post(API_URL, data=data)
        if response.status_code != 200:
            print(f"Failed to send alert: {response.status_code}")
    except Exception as e:
        print(f"Error while sending alert: {e}")

def check_market_condition():
    """Check market condition (this should be updated with real market conditions)"""
    # TODO: Replace this with actual market condition check
    return False, "No alert: market condition not met"

def is_market_open():
    """Check if current time is during market hours"""
    now = datetime.datetime.now()
    start_time = datetime.time(9, 0)  # 9:00 AM
    end_time = datetime.time(13, 30)  # 1:30 PM
    return start_time <= now.time() <= end_time

while True:
    try:
        if is_market_open():
            # If market is open, check the market condition
            condition, msg = check_market_condition()
            if condition and not last_alert_sent:
                # If condition is met and no alert has been sent yet
                send_alert(msg)
                last_alert_sent = True
                last_alert_time = datetime.datetime.now()  # Update last alert time
                print(f"Alert sent at {last_alert_time}")
            else:
                # If market condition not met or alert already sent
                if last_alert_time and (datetime.datetime.now() - last_alert_time).seconds > 3600:  # 1 hour cooldown
                    # Reset alert if 1 hour passed since last alert
                    last_alert_sent = False
                print("No alert sent or cooldown period")
            time.sleep(60)  # Wait 1 minute before checking again
        else:
            print("Market is closed")
            time.sleep(60)  # Wait 1 minute if market is closed
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)  # Wait 1 minute before retrying
