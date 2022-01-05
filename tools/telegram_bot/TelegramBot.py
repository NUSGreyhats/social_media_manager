import json
import requests
from util import make_get_url, make_send_url, make_img_url


class TelegramBot(object):
    def __init__(self, token: str):
        self.token = token

    def get_message(self) -> list:
        url = make_get_url(self.token)
        resp = requests.get(url)

        if resp.status_code != 200:
            return []
        return json.loads(resp.content)

    def send_message(self, message: str, group_id: str):
        url = make_send_url(message, self.token, group_id)
        resp = requests.post(url)
        return resp

    def send_image(self, message: str, group_id: str, image_path: str):
        url = make_img_url(message, self.token, group_id)
        with open(image_path, 'rb') as f:
            resp = requests.post(url, files={"photo": f})
        return resp
