from facebook import GraphAPI


class FacebookBot(object):
    def __init__(self, token):
        """The base facebook bot"""
        self.graph = GraphAPI(access_token=token)

    def post_to_group(self, message: str, group_id: str):
        """Make a post to a group with just an image"""
        self.graph.put_object(group_id, 'feed', message=message, )
        print(self.graph.get_connections(group_id, 'feed'))

    def post_img_to_group(self, img_path: str, group_id: str, message: str):
        """Make a post with an image to a facebook group"""
        with open(img_path, 'rb') as f:
            self.graph.put_photo(
                f, album_path=f'/{group_id}/photos', message=message)
        print(self.graph.get_connections(group_id, 'feed'))
