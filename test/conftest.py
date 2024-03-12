import os
from dotenv import load_dotenv
import pytest

from src import create_app, db

load_dotenv()
@pytest.fixture
def app():
    app = create_app(db_url=os.getenv('TEST_DATABASE_URL'))
    app.config.update(TESTING=True)
    return app

# Define a test client to interact with the app
@pytest.fixture
def client(app):
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        if "test" in app.config["SQLALCHEMY_DATABASE_URI"]:
            db.reflect()
            db.drop_all()

# Define a fixture for the token header
@pytest.fixture
def auth_header(client, user_data):
    # Register and login a user to obtain an access token
    client.post('/register', json=user_data)
    response = client.post('/login', json=user_data)
    access_token = response.json['access_token']

    # Return the authorization header with the access token
    return {'Authorization': f'Bearer {access_token}'}

# Define a test user data
@pytest.fixture
def user_data():
    return {'username': 'test_user', 'password': 'test_password'}

@pytest.fixture
def store_data():
    return {'name': 'Test Store'}

# Define a fixture to create a store and return its ID
@pytest.fixture
def store_id(client, store_data):
    response = client.post('/store', json=store_data)
    return response.json['id']

# Define a test item data
@pytest.fixture
def item_data(store_id):
    return {'name': 'Test Item', 'price': 9.99, 'store_id': store_id}

# Define a fixture to create an item and return its ID
@pytest.fixture
def item_id(client, item_data, auth_header):
    response = client.post('/item', json=item_data, headers=auth_header)
    return response.json['id']

# Define a test tag data
@pytest.fixture
def tag_data():
    return {'name': 'Test Tag'}

# Define a fixture to create a tag and return its ID
@pytest.fixture
def tag_id(client, tag_data, store_id):
    response = client.post(f'/store/{store_id}/tag', json=tag_data)
    return response.json['id']