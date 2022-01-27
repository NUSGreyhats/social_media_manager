from . import TwitterBot, TelegramBot, FacebookBot


def post_to_twitter(api_key: str, api_secret: str, access_token: str, access_token_secret: str, message: str, image: str = None, **kwargs) -> None:
    """Post to Twitter with an optional image"""
    print("Twitter is not supported yet, sorry!")
    return
    # bot = TwitterBot(api_key, api_secret, access_token, access_token_secret)
    # if image is None:
    #     bot.tweet_message(message)
    # else:
    #     bot.tweet_image(message, image)


def post_to_telegram(token: str, group_id: str, message: str, image: str = None, **kwargs) -> None:
    """Post to Telegram"""
    bot = TelegramBot(token)
    if image is None:
        bot.send_message(message, group_id)
    else:
        bot.send_image(message, group_id, image)


def post_to_facebook(token: str, group_id: str, message: str, image: str = None, **kwargs) -> None:
    """Post to Facebook"""
    bot = FacebookBot(token)
    if image is None:
        bot.post_to_group(message, group_id)
    else:
        bot.post_img_to_group(image, group_id, message)
