import pytest
from app import app
import multiprocessing
from unittest.mock import patch, MagicMock

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

def test_run_generate_commit(client, mocker):
    mocker.patch('subprocess.run', return_value=mocker.Mock(stdout="Success", stderr="", returncode=0))
    rv = client.get('/run-generate-commit')
    assert rv.status_code == 200
    assert rv.get_json() == {"stdout": "Success", "stderr": "", "returncode": 0}

def test_run_generate_commit_error(client, mocker):
    mocker.patch('subprocess.run', side_effect=Exception("Test Error"))
    rv = client.get('/run-generate-commit')
    assert rv.status_code == 500
    assert rv.get_json() == {"error": "Test Error"}

def run_app():
    app.run(host='0.0.0.0', port=80)

def test_main():
    p = multiprocessing.Process(target=run_app)
    p.start()
    p.terminate()
    p.join()

