import requests
from secrets import TOKEN
from facebook import GraphAPI


class FacebookBot(object):
    def __init__(self, token):
        self.graph = GraphAPI(access_token=token)

    def post_to_group(self, message: str, group_id: str):
        self.graph.put_object(group_id, 'feed', message=message)
        print(self.graph.get_connections(group_id, 'feed'))


if __name__ == "__main__":
    bot = FacebookBot(TOKEN)
    bot.post_to_group("Hello world", 582637322737005)
