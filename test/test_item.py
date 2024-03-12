import pytest


def test_create_item(client, item_data, auth_header):
    response = client.post('/item', json=item_data, headers=auth_header)
    assert response.status_code == 201
    assert 'name' in response.json
    assert 'price' in response.json

# Test getting an item
def test_get_item(client, item_id, auth_header):
    response = client.get(f'/item/{item_id}', headers=auth_header)
    assert response.status_code == 200
    assert 'name' in response.json
    assert 'price' in response.json

# Test updating an item
def test_update_item(client, item_id):
    updated_data = {'name': 'Updated Item', 'price': 19.99}
    response = client.put(f'/item/{item_id}', json=updated_data)
    assert response.status_code == 200
    assert 'name' in response.json
    assert 'price' in response.json
    assert response.json['name'] == updated_data['name']
    assert response.json['price'] == updated_data['price']

# Test getting the list of items
def test_get_items(client, item_data, auth_header):
    # Create an item for the test
    client.post('/item', json=item_data, headers=auth_header)

    response = client.get('/item', headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1

# Test deleting an item
def test_delete_item(client, item_id, auth_header):
    response = client.delete(f'/item/{item_id}', headers=auth_header)
    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Item deleted successfully.'

    # Verify that the item is no longer in the list
    response = client.get('/item', headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 0


# xfail tests
@pytest.mark.xfail
def test_create_item_xfail(client, item_data):
    # This test is expected to fail
    response = client.post('/item', json=item_data)
    assert response.status_code == 500

@pytest.mark.xfail
def test_get_item_xfail(client, item_id):
    # This test is expected to fail
    response = client.get(f'/item/{item_id}')
    assert response.status_code == 404 