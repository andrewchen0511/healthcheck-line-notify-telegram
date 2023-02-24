#!/usr/bin/python
import datetime
import requests
import os

# All of healthcheck API欲監控之api及其正常的statuscode
apilist = [
    {'website':"https://...../api/token/", 'statuscode':400, "method":requests.post, "data":{"username": "","password": ""}},
    {'website':"https://...../health", 'statuscode':200, "method":requests.get, "data":{}},
    {'website':"https://...../staging/.../health", 'statuscode':200, "method":requests.get, "data":{}}


]
# standard time def
def time():
    try:
        # Getting the standard time upto seconds only.
        global Standard_time
        Standard_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'Standard Time:{Standard_time}(UTC +8:00)')
    except:
        print('Something Wrong in main function',exc_info=True)

if __name__=='__main__':
    time()

# Send-message-to-Line-Notify Function
def send_to_line(message):
    # K8s Secert env Inject # Line Notify API Token
    lineToken = os.getenv('lineToken')
    # HTTP Head parameter & data
    headers = { "Authorization": "Bearer " + lineToken }
    requests.post("https://notify-api.line.me/api/notify", headers = headers, data = { 'message':message })

# Send-message-to-telegram Function
# Check ID website https://api.telegram.org/bot5834396372:AAFX3-TbwkK6Mhf8qfMANi-lOJAeGADyYgo/getUpdates
def send_to_telegram(message):
    # WebHealthCheck-notification-popoint Chat Group ID : <Add your ID>
    chatID = '<Add your ID>'
    # PoService-AlarmBot's apiToken
    apiToken = os.getenv('apiToken')
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)


def api_path(api_website, statuscode, method, data):
    r = method(url=api_website,data = data)
    print(api_website, r.status_code)
    if r.status_code != int(statuscode):
        # Line Alarm Messenge
        send_to_line(f'ALARM!!! \nStandard Time:{Standard_time}(UTC +8:00) \nin Production.{str(api_website)}\nThis API is disconnect. StatusCode is {str(r.status_code)} \nPlease Check APISIX Status\n')
        # telegram Alarm Messenge
        send_to_telegram(f'ALARM!!! \nStandard Time:{Standard_time}(UTC +8:00) \nin Production.{str(api_website)}\nThis API is disconnect. StatusCode is {str(r.status_code)} \nPlease Check APISIX Status\n')
        print(str(api_website) + '\n This API is disconnect. ' + 'StatusCode is ' + str(r.status_code))
    
for i in range(0,len(apilist)):
    api_path(apilist[i]['website'], apilist[i]['statuscode'], apilist[i]['method'], apilist[i]['data'])
