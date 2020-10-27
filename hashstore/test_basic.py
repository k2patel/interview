import os
import sys
sys.path.append(".")
import pytest
from app import app
import json

@pytest.fixture
def client():
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, There is nothing here' in response.data

def test_messages(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "message": "tedst"
        }
    url = '/messages'

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert b'e8bff0e6f633d4b97c0693dff0ec91dc4b4f13c57610f112fc225f6d3458823a' in response.data


def test_messages1(client):
    url = '/messages/e8bff0e6f633d4b97c0693dff0ec91dc4b4f13c57610f112fc225f6d3458823a'

    response = client.get(url)
    assert b'tedst' in response.data