from ...inventory_management.app.dummy_products import dummy_products as dummy_products
import tests.utils as utils


#dummy_products_data = dummy_products.get_dummy_data()

dummy_products_data = utils.get_all_products()

def test_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200

def test_get_all_orders(client):
    response = client.get('/orders')

    # url = f"http://localhost:8004/orders"
    # response = requests.get(url)
    product_details = json.loads(response.content.decode('utf-8'))['value']

    # POST request to '/users' to register a new user
    response = client.get('/orders', data=json.dumps(user_data), content_type='application/json')


def test_get_order_by_id(client):
    order_id = ''
    response = client.get(f"/orders/{order_id}") 
    pass

def test_add_order(client):
    # Setup: Create a table and add an item
    

    user_data = {
     "user_id": "username_test",
     "product_id": dummy_products_data[0]['product_id'],
     "quantity": 7
    }
    # POST request to '/users' to register a new user
    response = client.post('/users', data=json.dumps(user_data), content_type='application/json')
    # Check if the request was successful
    assert response.status_code == 200
    response_json = response.get_json()
    assert response.json['status'] == True
    assert 'user_id' in response_json['value'], "user_id key is missing in the response"
    assert response_json['value']['address'] == user_data['address']
    assert response_json['value']['email'] == user_data['email']
    assert response_json['value']['phone'] == user_data['phone']
    assert response_json['value']['profile_picture'] == ""
    assert response_json['value']['type'] == "User"
    assert response_json['value']['username'] == user_data['username']


def test_update_order(client):
    pass


def test_delete_order(client):
    pass


def test_update_order_status(client):
    #check orders status changed

    #check po order status changed
    pass

def test_search_user_order_by_status(client):
    pass

def test_search_po_order_by_status(client):
    pass



def search_po_orders_by_po_id(client):
    pass