# Test creating a store
def test_create_store(client, store_data, auth_header):
    response = client.post('/store', json=store_data, headers=auth_header)
    assert response.status_code == 201
    assert 'name' in response.json
    assert 'id' in response.json

# Test getting a store
def test_get_store(client, store_id, auth_header):
    response = client.get(f'/store/{store_id}', headers=auth_header)
    assert response.status_code == 200
    assert 'name' in response.json
    assert 'id' in response.json

# Test getting the list of stores
def test_get_stores(client, store_data, auth_header):
    # Create a store for the test
    client.post('/store', json=store_data, headers=auth_header)

    response = client.get('/store', headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1

# Test deleting a store
def test_delete_store(client, store_id, auth_header):
    response = client.delete(f'/store/{store_id}', headers=auth_header)
    assert response.status_code == 200
    assert 'message' in response.json
    assert response.json['message'] == 'Store deleted successfully.'

    # Verify that the store is no longer in the list
    response = client.get('/store')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 0