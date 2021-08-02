from urllib.parse import quote_plus
from constants import TELEGRAM_GET_ENDPOINT, TELEGRAM_SEND_ENDPOINT, TELEGRAM_SEND_PHOTO_ENDPOINT


def make_get_url(token: str) -> str:
    return TELEGRAM_GET_ENDPOINT.format(token=token)


def make_send_url(message: str, token: str, group_id: str) -> str:
    return TELEGRAM_SEND_ENDPOINT.format(message=quote_plus(message), token=token, group_id=group_id)


def make_img_url(message: str, token: str, group_id: str) -> str:
    return TELEGRAM_SEND_PHOTO_ENDPOINT.format(token=token, caption=message, group_id=group_id)
