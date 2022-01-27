from tweepy import OAuthHandler, API


class TwitterBot:
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        auth = OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = API(
            auth,
            wait_on_rate_limit=True,
        )
        self.verify()

    def verify(self) -> None:
        """Verify the credentials"""
        self.api.verify_credentials()

    def tweet_message(self, message: str) -> None:
        """Tweet a message"""
        self.api.update_status(message)

    def tweet_image(self, message: str, img_path: str) -> None:
        """Tweet a message with an image"""
        self.api.update_with_media(img_path, message)
