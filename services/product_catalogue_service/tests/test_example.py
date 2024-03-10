def test_get_example(client):
    response = client.get('/products')
    assert response.status_code == 200
    
def test_post_example(client):
    data = {"key": "value"}
    response = client.post('/product/new', json=data)
    assert response.status_code == 200