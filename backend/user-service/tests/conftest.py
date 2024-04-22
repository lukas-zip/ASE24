import pytest

@pytest.fixture()
@pytest.fixture()
def app():
    from app import app
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()