"""The frontend for the social media manager"""
import os
import configparser
from flask import Flask, render_template, request, redirect, flash, Response

from constants import ERROR_FLASH, FACEBOOK, IMAGE_KEY, INFO_FLASH, SOCIAL_MEDIA, HOME_PAGE, SELECT_AT_LEAST_ONE_SOCIAL_MEDIA, SUCCESS_MESSAGE, EMPTY_CONTENT, CONTENT_KEY, EMPTY_STRING, DEFAULT_CONFIG_FILE, TELEGRAM, TWITTER
from tools import post_to_twitter


app = Flask(__name__)
app.secret_key = os.urandom(128).hex()
credentials = None


@app.route('/', methods=['GET', 'POST'])
def index() -> Response:
    """The home page for the social media manager"""
    if request.method == "GET":
        return render_template('index.html')

    # Check if the content is empty
    if len(request.form.get(CONTENT_KEY, EMPTY_STRING)) == 0:
        flash(EMPTY_CONTENT, ERROR_FLASH)
        return redirect(HOME_PAGE)

    # Check if user picked at least one social media.
    to_post = set()
    for attr in request.form:
        if attr in SOCIAL_MEDIA:
            to_post.add(attr)
            break
    else:
        flash(SELECT_AT_LEAST_ONE_SOCIAL_MEDIA, ERROR_FLASH)
        return redirect(HOME_PAGE)

    # Logic for posting items to social media.
    if TWITTER in to_post:
        post_to_twitter(
            **credentials[TWITTER],
            content=request.form.get(CONTENT_KEY),
            image=request.files.get(IMAGE_KEY)
        )

    if FACEBOOK in to_post:
        pass

    if TELEGRAM in to_post:
        pass

    flash(SUCCESS_MESSAGE, INFO_FLASH)
    return redirect(HOME_PAGE)


def create_default_config() -> None:
    """Create a default configuration file"""
    config = configparser.ConfigParser()
    config["twitter"] = {
        "api_key": "",
        "api_secret": "",
        "access_token": "",
        "access_token_secret": "",
        "bearer_token": "",
    }
    config["facebook"] = {
        "token": "",
        "group_id": "",
    }
    config["telegram"] = {
        "api_token": "",
        "group_id": "",
    }
    with open(DEFAULT_CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        create_default_config()
    credentials = configparser.ConfigParser()
    credentials.read(DEFAULT_CONFIG_FILE)
    app.run(debug=False)
