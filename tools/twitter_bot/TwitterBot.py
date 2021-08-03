import tweepy
from secrets import API_SECRET_KEY, API_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

class TwitterBot(object):
    def __init__(self, api_key, api_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def verify(self):
        self.api.verify_credentials()

    def tweet_message(self, message: str):
        self.api.update_status(message)
    
    def tweet_image(self, message: str, img_path: str):
        with open(img_path, 'rb') as f:
            resp = self.api.upload_media(media=f)
        self.api.update_status(message, resp.get('media_id'))


if __name__ == "__main__":
    bot = TwitterBot(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    bot.tweet_message("Hi guys, we are back")
    bot.tweet_image("We will be posing some exciting content soon", "D:\Downloads\logo.png")