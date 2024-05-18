import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert rv.data == b'Hello, World!'

def test_error(client):
    rv = client.get('/error')
    assert rv.status_code == 400
    assert rv.get_json() == {"error": "This is an error message"}
