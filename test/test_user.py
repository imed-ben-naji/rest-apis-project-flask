import pytest
from src import create_app


# Test user registration and login
def test_register_and_login(client, user_data):
    # Register a user
    response = client.post('/register', json=user_data)
    assert response.status_code == 200
    assert 'User created successfully.' in response.json['message']

    # Login with the registered user
    response = client.post('/login', json=user_data)
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json