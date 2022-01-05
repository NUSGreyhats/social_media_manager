from constants import FACEBOOK_GROUP_URL


def create_group_url(group_id: str):
    return FACEBOOK_GROUP_URL.format(group_id = group_id)