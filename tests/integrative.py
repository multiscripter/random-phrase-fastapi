from controller import app
from fastapi.testclient import TestClient
import re

# pytest -p no:cacheprovider integrative.py

client = TestClient(app)


def test_get_success():
    """Test: Method GET, URI /get"""

    response = client.get('http://127.0.0.1:8000/get')
    assert response.status_code == 200

    actual = response.json()
    assert re.match('test-text', actual['text'])


def test_add_success():
    """Test: Method POST, URI /add"""

    data = {
        "author": "Fake",
        "text": "Foo"
    }
    response = client.post('http://127.0.0.1:8000/add', json=data)
    assert response.status_code == 201

    actual = response.json()
    assert data['text'] == actual['text']


def test_delete_error_element_is_not_exists():
    """Test: Method DELETE, URI /delete
    Error. Element is not exists."""

    response = client.delete('http://127.0.0.1:8000/delete/100500')
    assert response.status_code == 404

    actual = response.json()
    assert 'Element is not exists' == actual['detail']


def test_delete_success():
    """Test: Method DELETE, URI /delete"""

    response = client.delete('http://127.0.0.1:8000/delete/1')
    assert response.status_code == 200

    actual = response.json()
    assert 1 == actual


def test_update_success():
    """Test: Method PATCH, URI /update"""

    id = 2
    data = {
        "author": "new-author",
        "text": "new-text"
    }
    response = client.patch(f'http://127.0.0.1:8000/update/{id}', json=data)
    assert response.status_code == 205

    actual = response.json()
    assert id == actual['id']
    assert data['text'] == actual['text']
