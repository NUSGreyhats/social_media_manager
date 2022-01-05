from secrets import TOKEN
from facebook import GraphAPI


class FacebookBot(object):
    def __init__(self, token):
        self.graph = GraphAPI(access_token=token)

    def post_to_group(self, message: str, group_id: str):
        self.graph.put_object(group_id, 'feed', message=message, )
        print(self.graph.get_connections(group_id, 'feed'))

    def post_img_to_group(self, img_path:str, group_id:str, message:str):
        with open(img_path, 'rb') as f:
            self.graph.put_photo(f, album_path=f'/{group_id}/photos', message=message)
        print(self.graph.get_connections(group_id, 'feed'))


if __name__ == "__main__":
    bot = FacebookBot(TOKEN)
    # bot.post_to_group("Hello world", "582637322737005")
    # bot.post_img_to_group(r"D:\Downloads\welcome_tea.png", "582637322737005", "Welcome")
