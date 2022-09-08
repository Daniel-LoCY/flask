import requests
import json

def sent(message):

    # LINE Notify 權杖
    token = '3e7dgdsZpzPvC57MCP5JmmwuIkeDTaZactokhpzTKLX'

    # 要發送的訊息
    message = message

    # HTTP 標頭參數與資料
    headers = { "Authorization": "Bearer " + token }
    data = { 'message': message }

    # files = {}
    # with open('../甄試資料/1154x768_20210429000115.jpg', 'rb') as f:
    #     files['imageFile'] = f.read()
    # print(files)

    # 以 requests 發送 POST 請求
    requests.post("https://notify-api.line.me/api/notify", headers = headers, data = data)


# headers = {'accept':'application/vnd.heroku+json; version=3.account-quotas',
#             'authorization': 'Bearer aff1ab3a-3bbf-4422-8794-a8912420e746'}

# '''
# accept: application/vnd.heroku+json; version=3.account-quotas
# accept-encoding: gzip, deflate, br
# accept-language: zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7
# authorization: Bearer aff1ab3a-3bbf-4422-8794-a8912420e746
# origin: https://dashboard.heroku.com
# referer: https://dashboard.heroku.com/
# sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Windows"
# sec-fetch-dest: empty
# sec-fetch-mode: cors
# sec-fetch-site: same-site
# user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
# x-heroku-requester: dashboard
# x-origin: https://dashboard.heroku.com
# '''

# data = requests.get('https://api.heroku.com/accounts/cf95f010-a564-4e41-b26d-333b0ce69d4c/actions/get-quota', headers=headers)

# data_json = json.loads(data.text)

# #print(data_json)

# total = round(data_json['account_quota']/3600, 2)

# used = round(data_json['quota_used']/3600, 2)

# can_use = total - used

# message = f'\n本月Heroku用量報告:\n\n總共可用{total}個小時\n已使用{used}個小時\n剩餘{can_use}個小時'
# #print(message)
# sent(message)
