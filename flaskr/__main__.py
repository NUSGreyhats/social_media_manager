"""The frontend for the social media manager"""
import os
import configparser


try:
    from constants import DEFAULT_CONFIG_FILE, UPLOAD_FOLDER
    from app import app
except ImportError:
    from .constants import DEFAULT_CONFIG_FILE, UPLOAD_FOLDER
    from .app import app


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
    with open(DEFAULT_CONFIG_FILE, "w") as configfile:
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
