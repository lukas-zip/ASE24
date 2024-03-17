def test_get_example(client):
    response = client.get('/users')
    assert response.status_code == 200
    
def test_post_example(client):
    data = {"key": "value"}
    response = client.post('/user/register', json=data)
    assert response.status_code == 200