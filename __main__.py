"""The frontend for the social media manager"""
import logging
import os
import configparser
from flask import Flask, abort, render_template, request, redirect, flash, Response
from functools import partial
from werkzeug.utils import secure_filename

from constants import (
    BODY_KEY,
    CSV_KEY,
    EMAIL_KEY,
    ERROR_FLASH,
    FACEBOOK,
    IMAGE_KEY,
    INFO_FLASH,
    SOCIAL_MEDIA,
    HOME_PAGE,
    SELECT_AT_LEAST_ONE_SOCIAL_MEDIA,
    SUBJECT_KEY,
    SUCCESS_MESSAGE,
    EMPTY_CONTENT,
    CONTENT_KEY,
    EMPTY_STRING,
    DEFAULT_CONFIG_FILE,
    TELEGRAM,
    TWITTER,
    EMAIL_PAGE,
    UPLOAD_FOLDER,
)
from tools.post import post_to_facebook, post_to_telegram, post_to_twitter
from tools.email.email_sc import EmailIntegration, create_email
from tools.email import extract_csv
from tools.utils import replace_string


# Set up logger
logging.basicConfig(
    format="%(levelname)s:%(message)s",
    filename="server.log",
    encoding="utf-8",
    level=logging.DEBUG,
)


# Set up flask
app = Flask(__name__)
app.secret_key = os.urandom(128).hex()
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
credentials = None
email_server = None
func_dict = {
    FACEBOOK: post_to_facebook,
    TELEGRAM: post_to_telegram,
    # TWITTER: post_to_twitter,
}


@app.route("/email", methods=["GET", "POST"])
def email() -> Response:
    """The page for mass sending email"""
    if request.method == "GET":
        return render_template("email.html")

    # Ensure that the email server is set up.
    if email_server is None:
        logging.error("Email server not set up")
        return abort(
            500,
            "Email server not set up, please contact the administrator / check configuration",
        )

    subject = request.form.get(SUBJECT_KEY, None)
    body = request.form.get(BODY_KEY, None)
    csv_file = request.files.get(CSV_KEY, None)

    if (
        None in (subject, body, csv_file)
        or len(subject) == 0
        or len(body) == 0
        or len(csv_file.filename) == 0
    ):
        logging.error("Missing fields")
        flash(EMPTY_CONTENT, ERROR_FLASH)
        return redirect(EMAIL_PAGE)

    filepath = os.path.join(UPLOAD_FOLDER, secure_filename(csv_file.filename))
    csv_file.save(filepath)

    # Extract the CSV into a list of dictionaries
    header, data = extract_csv(filepath)
    os.remove(filepath)
    logging.info(f"Extracted {len(data)} rows from {filepath} with header {header}")

    if EMAIL_KEY not in header:
        logging.info("CSV file does not contain an email column")
        flash(f"{CSV_KEY} must contain a column named {EMAIL_KEY}", ERROR_FLASH)
        return redirect(EMAIL_PAGE)

    logging.info(f"Sending emails to {len(data)} recipients")
    # Get all keys
    error_count = 0
    for row in data:
        email = row.get("email", None)
        if email is None:
            error_count += 1
            continue

        # Format the email and send
        try:
            content_subject = replace_string(row, subject)
            content_body = replace_string(row, body)
        except KeyError as e:
            msg = f"{e} not found in {BODY_KEY}"
            logging.info(msg)
            flash(msg, ERROR_FLASH)
            return redirect(EMAIL_PAGE)
        except Exception as e:
            msg = f"Error formatting email: {e}"
            logging.error(f"{msg}. Subject: {subject}, body: {body}")
            flash(msg, ERROR_FLASH)
            return redirect(EMAIL_PAGE)

        mime_email = create_email(
            credentials["email"]["from_email"], [email], content_subject, content_body
        )

        # Send the email
        try:
            email_server.send_email(email, mime_email)
        except Exception as e:
            logging.error(f"Failed to send email to {email}: {e}")
            error_count += 1
            continue

        logging.info(
            f"Sent email to {email} with subject: {content_subject} and body {content_body}"
        )

    if error_count > 0:
        logging.info(
            f"{error_count} emails were not sent due to invalid/missing email addresses"
        )
        flash(
            f"{error_count} emails were not sent due to missing email addresses. Please check the logs",
            ERROR_FLASH,
        )
    else:
        logging.info(f"Sent {len(data)} emails")
        flash(SUCCESS_MESSAGE, INFO_FLASH)
    return redirect(EMAIL_PAGE)


@app.route("/", methods=["GET", "POST"])
def index() -> Response:
    """The home page for the social media manager"""
    if request.method == "GET":
        return render_template("index.html")

    is_success = True

    # Check if the content is empty
    if len(request.form.get(CONTENT_KEY, EMPTY_STRING)) == 0:
        logging.error("Missing content")
        flash(EMPTY_CONTENT, ERROR_FLASH)
        return redirect(HOME_PAGE)

    image = request.files.get(IMAGE_KEY, None)
    img_path = None

    if image is not None and image.filename != EMPTY_STRING:

        filename = secure_filename(image.filename)
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        logging.info(f"Image detected, saving to {img_path}")
        image.save(img_path)

    # Check if user picked at least one social media.
    to_post = set()
    for attr in request.form:
        if attr in SOCIAL_MEDIA:
            to_post.add(attr)

    if len(to_post) == 0:
        logging.error("No social media selected")
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
            logging.info(f"Successfully posted to {post_type}")
        except Exception as e:
            msg = f"Error posting to {post_type}: {e}"
            logging.error(msg)
            flash(msg, ERROR_FLASH)
            is_success = False

    # Remove the image after posting
    if img_path is not None:
        os.remove(img_path)
        logging.info(f"Removed image {img_path}")

    if is_success:
        logging.info(f"Successfully posted to {', '.join(to_post)}")
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
    config["email"] = {
        "smtp_host": "",
        "smtp_port": "",
        "username": "",
        "password": "",
        "from_email": "",
    }
    with open(DEFAULT_CONFIG_FILE, "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    logging.info("Starting server")

    # Read Config File
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        create_default_config()
        logging.info(f"Created default configuration file at {DEFAULT_CONFIG_FILE}")
    credentials = configparser.ConfigParser()
    credentials.read(DEFAULT_CONFIG_FILE)
    logging.info("Read configuration file")

    # Setup email connection
    logging.info("Setting up email connection to smtp server")
    email_credentials = credentials["email"]
    try:
        email_server = EmailIntegration(
            email_credentials["smtp_host"],
            email_credentials["smtp_port"],
            email_credentials["username"],
            email_credentials["password"],
            email_credentials["from_email"],
        )
    except Exception as e:
        logging.error(f"Error starting email service: {e}")
        raise e

    # Check if upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        logging.info(f"Creating upload folder: {UPLOAD_FOLDER}")
        os.mkdir(UPLOAD_FOLDER)

    # Starting the app
    logging.info("Starting the application")
    app.run(debug=False)
