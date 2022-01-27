"""The frontend for the social media manager"""
import os
import configparser
from flask import Flask, render_template, request, redirect, flash, Response
from werkzeug.utils import secure_filename

from constants import ERROR_FLASH, FACEBOOK, IMAGE_KEY, INFO_FLASH, SOCIAL_MEDIA, HOME_PAGE, SELECT_AT_LEAST_ONE_SOCIAL_MEDIA, SUCCESS_MESSAGE, EMPTY_CONTENT, CONTENT_KEY, EMPTY_STRING, DEFAULT_CONFIG_FILE, TELEGRAM, TWITTER, UPLOAD_FOLDER 
from tools import post_to_twitter
from tools.post import post_to_facebook, post_to_telegram


app = Flask(__name__)
app.secret_key = os.urandom(128).hex()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
credentials = None
func_dict = {
    FACEBOOK: post_to_facebook,
    TELEGRAM: post_to_telegram,

    # TWITTER: post_to_twitter,
}


@app.route('/', methods=['GET', 'POST'])
def index() -> Response:
    """The home page for the social media manager"""
    if request.method == "GET":
        return render_template('index.html')

    is_success = True

    # Check if the content is empty
    if len(request.form.get(CONTENT_KEY, EMPTY_STRING)) == 0:
        flash(EMPTY_CONTENT, ERROR_FLASH)
        return redirect(HOME_PAGE)

    image = request.files.get(IMAGE_KEY, None)
    img_path = None

    if image is not None and image.filename != EMPTY_STRING:
        filename = secure_filename(image.filename)
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(img_path)


    # Check if user picked at least one social media.
    to_post = set()
    for attr in request.form:
        if attr in SOCIAL_MEDIA:
            to_post.add(attr)

    if len(to_post) == 0:
        flash(SELECT_AT_LEAST_ONE_SOCIAL_MEDIA, ERROR_FLASH)
        return redirect(HOME_PAGE)

    # Logic for posting items to social media.
    for post_type in to_post:
        try:
            func = func_dict[post_type]
            func(
                **credentials[post_type],
                message=request.form.get(CONTENT_KEY),
                image=img_path,
            )
        except Exception as e:
            flash(f"Error posting to {post_type}: {e}", ERROR_FLASH)
            is_success = False
    
    # Remove the image after posting
    if img_path is not None:
        os.remove(img_path)

    if is_success:
        flash(SUCCESS_MESSAGE, INFO_FLASH)
    return redirect(HOME_PAGE)


def create_default_config() -> None:
    """Create a default configuration file"""
    config = configparser.ConfigParser()
    # config["twitter"] = {
    #     "api_key": "",
    #     "api_secret": "",
    #     "access_token": "",
    #     "access_token_secret": "",
    #     "bearer_token": "",
    # }
    config["facebook"] = {
        "token": "",
        "group_id": "",
    }
    config["telegram"] = {
        "token": "",
        "group_id": "",
    }
    with open(DEFAULT_CONFIG_FILE, 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        create_default_config()
    credentials = configparser.ConfigParser()
    credentials.read(DEFAULT_CONFIG_FILE)

    # Check if upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    app.run(debug=False)
