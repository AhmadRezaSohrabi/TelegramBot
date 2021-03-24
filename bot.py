import json

import requests

from app_config import BOT_TOKEN, TELEGRAM_BOT_ROOT_URL

from utils import validated_url

class BotAPI:
    def __init__(self, chat_id):
        self.chat_id = chat_id
    
    def send_query_result(self, text):
        url = '{root_url}/bot{token}/sendMessage'.format(
            root_url=validated_url(TELEGRAM_BOT_ROOT_URL),
            token=BOT_TOKEN,
        )

        data = {
            'chat_id': self.chat_id,
            'text': text or 'Empty Query!',
        }
        res = requests.post(url, data=json.dumps(data), headers={'content-type': 'application/json'},verify=False)
        if res:
            print('==> Success')
            print(res.text)
        else:
            print('==> Failed')
            print(res.text)


