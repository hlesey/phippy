from time import sleep
import pytest

import os
import json
import redis as redis
from src.api import app as flask_app


redis_container = {}

@pytest.fixture()
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
