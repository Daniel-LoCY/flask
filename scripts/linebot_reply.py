import json
import requests

def reply(replyToken, message = ''):
    token = 'npoXB7/91zMn5U38wJDRr3mL0WCs7IurlpmKQPX5AgYrcwfIJNvGzXKE3Of+akZopiE2YvYzIbO4tp4trDnC/1Y5eK1AL3yZra8J2sEfL8La5o5tpI33IK1P7loKNxwvyMyMEK9Nrv9qACcY8WJ4IQdB04t89/1O/w1cDnyilFU='

    headers = { 'Authorization': 'Bearer ' + token, 'Content-Type':'application/json'}

    replyText = message if message != '' else message

    data = { 
        'replyToken' : replyToken,
        'messages' : [
            {
                'type' : 'text',
                'text' : replyText
            }
        ]
    }

    data = json.dumps(data)

    response = requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, data=data)
    
    return response