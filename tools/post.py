from . import TwitterBot

def post_to_twitter(api_key:str, api_secret:str, access_token:str, access_token_secret:str, content:str, image:str = None, **kwargs) -> None:
    """Post to Twitter with an optional image"""
    bot = TwitterBot(api_key, api_secret, access_token, access_token_secret)
    if image is None:
        bot.tweet_message(content)
    else:
        bot.tweet_image(content, image)
