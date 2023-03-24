#!/usr/bin/python
import datetime
import os
import requests
from typing import Dict
from concurrent.futures import ThreadPoolExecutor, as_completed


# Constants
CHAT_ID = "-10017......"  # WebHealthCheck-notification-popoint Chat Group ID 
LINE_TOKEN = os.getenv('lineToken')  # K8s Secret env Inject # Line Notify API Token
TELEGRAM_Bot_TOKEN = os.getenv('apiToken')  # PoService-AlarmBot's apiToken
API_HEALTH_CONFIG = {
    "https://website": {
        "status_code": 400,
        "method": requests.post,
        "data": {"username": "", "password": ""},
    },
    "https://website": {"status_code": 200, "method": requests.get, "data": {},},
}

# Get standard time in the format of 'Y-m-d H:M:S (UTC +0:00)'
def get_standard_time() -> str:
    try:
        return f'Standard Time:{datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} (UTC +0:00)'
    except Exception as e:
        print('Something Wrong in get_standard_time function', exc_info=True)
        
# Send message to Line Notify
def send_to_line(message: str):
    headers = {"Authorization": f"Bearer {LINE_TOKEN}"}
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data={"message": message})
    
# Send message to Telegram
def send_to_telegram(message: str):
    chat_id = CHAT_ID
    api_url = f"https://api.telegram.org/bot{TELEGRAM_Bot_TOKEN}/sendMessage"
    try:
        response = requests.post(api_url, json={"chat_id": chat_id, "text": message})
        response.raise_for_status()
        # print(response.text)
    except requests.exceptions.HTTPError as e:
        print(f"Error sending message to Telegram: {e}")
    except Exception as e:
        print(f"Unexpected error sending message to Telegram: {e}")

def check_api_health(api_website: str, status_code: int, method: object, data: Dict):
    r = method(url=api_website, data=data, timeout=(5, 10))
    print(api_website, r.status_code)
    if r.status_code != status_code:
        # Line and Telegram Alarm Messages
        std_time = get_standard_time()
        message = (
            f"ALARM!!!\nStandard Time: {std_time} (UTC +8:00)\n"
            f"in Production. {api_website}\nThis API is disconnected. StatusCode is {r.status_code}\n"
            "Please Check APISIX Status\n"
        )
        send_to_line(message)
        send_to_telegram(message)
        print(f"{api_website}\nThis API is disconnected. StatusCode is {r.status_code}")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=len(API_HEALTH_CONFIG)) as executor:
        futures = []
        for api, config in API_HEALTH_CONFIG.items():
            future = executor.submit(check_api_health, api, config["status_code"], config["method"], config["data"])
            futures.append(future)
        
        for future in as_completed(futures):
            result = future.result()
