import pytest
from flaskr import app as flask_app

@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield flask_app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()