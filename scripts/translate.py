import requests, uuid, json

def en_to_ch(word: str) -> str:
    # Add your subscription key and endpoint
    subscription_key = "50bb340474dc43959cbb21420e02e514"
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "eastus"

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': ['zh-Hant']
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    if word[:4] == 'tl: ':
        word = word[4:]
    else:
        return word
    body = [{
        'text': word
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    response = json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
    response = json.loads(response)
    
    ch_text = response[0]['translations'][0]['text']

    return ch_text