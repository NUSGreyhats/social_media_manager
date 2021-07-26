import json
import requests
from util import make_get_url, make_send_url

class TelegramBot(object):
    def __init__(self, token:str):
        self.token = token

    def get_message(self) -> list:
        url = make_get_url(self.token)
        resp = requests.get(url)

        if resp.status_code != 200:
            return []
        return json.loads(resp.content)

    def send_message(self, message:str, group_id: str) -> int:
        url = make_send_url(message, self.token, group_id)
        resp = requests.post(url)
        return resp.status_code
