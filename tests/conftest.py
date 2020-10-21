import pytest
from app import create_app
from db import db

@pytest.fixture
def app():
    current_app = create_app()
    return current_app

@pytest.fixture
def client():
    current_app = create_app()
    current_app.config['TESTING'] = True

    with current_app.test_client() as clnt:
        with current_app.app_context():
            db.init_app(current_app)
            yield clnt

