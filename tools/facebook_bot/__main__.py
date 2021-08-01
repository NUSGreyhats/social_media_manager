import requests
from constants import FACEBOOK_GROUP_URL


def generate_url(group_id: str) -> str:
    return FACEBOOK_GROUP_URL.format(group_id=group_id)


def post_to_group(access_token: str, message: str, group_id: str):
    url = generate_url(group_id)
    requests.post(url, message)
    # Todo send the msg to the endpoint


if __name__ == "__main__":
    pass
