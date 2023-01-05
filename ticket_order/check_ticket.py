import re
import requests
from bs4 import BeautifulSoup
from azure_database_exec import exec_database
from line_notify import sent

a = requests.post('https://www.ebus.com.tw/NetOrderURL/payOrder/selectOrder.aspx', data={
    'txtCId':'S125357579',
    'txtCTel': '0902170772',
    'txtChkCode': '0402',
    '__VIEWSTATE': '/wEPDwUKLTc3MTE2ODM0OA9kFgICAw9kFgICAQ9kFgQCAg9kFgJmD2QWAmYPZBYCAgEPZBYCZg9kFgJmDzwrAA0AZAIDD2QWAmYPZBYCZg9kFgICAQ9kFgJmD2QWAgIDDzwrAA0AZBgCBQtndk9yZGVyRGF0YQ88KwAKAgNmCAL/////D2QFCWd2UGF5RGF0YQ88KwAKAgNmCAL/////D2T905gzRHBCdUbWd2yHoA6LFhTpBg==',
    '__VIEWSTATEGENERATOR': 'FA868928',
    'butQuery': '下一步'
}, headers={
    'cookie': '_ga=GA1.3.503156391.1672803284; _gid=GA1.3.1144637547.1672803284; CheckCode=0402'
})
soup = BeautifulSoup(a.text, 'html.parser')

# with open('1.html', 'r') as f:
#     a = f.read()

# soup = BeautifulSoup(a, 'html.parser')

# print(soup.prettify())
s = ''

th = soup.find_all('th')
font = soup.find_all('font')
li = soup.find_all('li')[0]

pattern = re.compile(r'[\u4E00-\u9FFF]+')
font_pattern = re.compile(r'>(\S+)<')

situation = font_pattern.findall(str(li))
situation1 = situation[1].split('<')[0]

title = []
# print('')
for i in th:
    result = pattern.search(str(i))
    if result != None:
        title.append(result.group(0))

# print(title)

data = []
# print('')
for i in font:
    result = font_pattern.search(str(i))
    if result != None and '<b>' not in result.group(0):
        data.append(result.group(0).replace('>', '').replace('<', ''))

data.pop(0)
data.pop(0)
# print(data)
count = int(len(data)/len(title))
# print(count) # 訂單數

if count == 0: 
    exit('no order')

result = {}
for i in range(len(title)):
    l = []
    for j in range(count): 
        l.append(data[i+j*len(title)])
    result[title[i]] = l
# print(result)

order = {
    'travel_date': '乘車日期',
    'travel_time': '班次',
    'boarding': '上車地點',
    'get_off': '下車地點',
    'seat': '座位',
    'name': '乘客姓名',
    'ticket': '票種',
    'price': '票價',
    'coupon': '折價券',
    'ticket_num': '票號',
    'order_num': '訂單編號'
}

same = []

for i in range(count):
    sql = 'SELECT * FROM ticket_order WHERE id>=0'
    sql_insert = 'INSERT INTO ticket_order VALUES (0'
    for j in order.keys():
        sql += f" and {j}='{result[order[j]][i]}'"
        sql_insert += f", '{result[order[j]][i]}'"
    # print(sql)
    r = exec_database(sql)
    if len(r) != 0:
        same.append(True)
    else:
        same.append(False)
        sql_insert += ');'
        print('insert data')
        exec_database(sql_insert)
if len(same) > 1:
    for i in range(len(same)-1):
        _same = same[i] and same[i+1] 
else:
    _same = same[0]

s += f'\n共有{count}筆訂單\n'
s += f'{situation[0]} {situation1}\n'
for i in range(count):
    s += f'\n第{i+1}筆\n'
    for j in range(len(title)):
        s += f'{title[j]}: {result[title[j]][i]}\n'
    s += '\n'
# print(s)
if not _same:
    sent(s)

