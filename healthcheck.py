#!/usr/bin/python
import datetime
import requests
import os

# CronJob def會print出當下的時間
def main():
    try:
        # Getting the current time upto seconds only.
        global Current_time
        Current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('Current Time : ',Current_time)
    except:
        print('Something Wrong in main function',exc_info=True)

if __name__=='__main__':
    main()

# Mentor Prodction BIreport API
API_ENDPOINT = "輸入你要爬或打API的網址" 
data = {"username": "",
        "password": ""}
r = requests.post(url = API_ENDPOINT, data = data)
print(r.status_code)

# Secert env Inject
# 要通知的Line Notify API Token
lineToken = os.getenv('lineToken')
# telegram 的 Bot's apiToken
apiToken = os.getenv('apiToken')

# Send messenge text
message = '\n Current Time :' + Current_time + 'Line的通知訊息'
# HTTP Head parameter & data
headers = { "Authorization": "Bearer " + lineToken }
data = { 'message': message }

# Send-message-to-telegram Function
def send_to_telegram(message):
    chatID = '輸入你要telegram bot'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': 'Current Time :' + Current_time + message})
        # print(response.text)
    except Exception as e:
        print(e)

if r.status_code != int(400):
    # 以 requests send POST request
    requests.post("https://notify-api.line.me/api/notify", headers = headers, data = data)
    send_to_telegram( 'telegram的通知訊息')