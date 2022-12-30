import json
import datetime
import requests

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


url ='https://網址'
Token_ID = "輸入token ID"

headers = { "Authorization": "Bearer " + Token_ID }
data = {
    "page_size": 10,
    "start_date": "2022-11-30T06:17:26Z",
    "end_date": "2022-12-30T06:17:26Z"
}
r = requests.get(url=url,params=data,headers=headers)

print(r.status_code)
print(r.text)
