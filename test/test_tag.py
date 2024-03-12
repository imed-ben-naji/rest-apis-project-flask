# Test creating a tag
def test_create_store_tag(client, tag_data, store_id):
    response = client.post(f'/store/{store_id}/tag', json=tag_data)
    assert response.status_code == 201
    assert 'name' in response.json
    assert 'id' in response.json

# Test linking a tag to an item
def test_link_tag_to_item(client, item_id, tag_id):
    response = client.put(f'/item/{item_id}/tag/{tag_id}')
    assert response.status_code == 200
    

# Test unlinking a tag from an item
def test_unlink_tag_from_item(client, item_id, tag_id):
    client.put(f'/item/{item_id}/tag/{tag_id}')
    response = client.delete(f'/item/{item_id}/tag/{tag_id}')
    # print(response)
    # assert response.status_code == 200
    # assert 'message' in response
    # assert response.json['message'] == 'Tag removed from item successfully.'

# Test getting a tag
def test_get_tag(client, tag_id):
    response = client.get(f'/tag/{tag_id}')
    assert response.status_code == 200
    assert 'name' in response.json
    assert 'id' in response.json

# Test getting the list of tags
def test_get_store_tags(client, store_id, tag_data):
    response = client.post(f'/store/{store_id}/tag', json=tag_data)
    response = client.get(f'/store/{store_id}/tag')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 1

# Test deleting a tag
def test_delete_tag(client, tag_id):
    response = client.delete(f'/tag/{tag_id}')
    assert response.status_code == 201
    assert 'message' in response.json
    assert response.json['message'] == 'Tag deleted successfully.'