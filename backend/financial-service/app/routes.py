from app import app, dynamodb
from botocore.exceptions import ClientError
from flask_mail import Mail, Message
import requests
import json
from flask import jsonify, request
import stripe
import logging

# This is your test secret API key.
stripe.api_key = 'sk_test_51P3x1RL2VoulaBDdRpHDMZQCFlvnAmG1D1HRzjwnual8vUucfqdIRJiuMDGXOcVP5m6zwvaYPE6QzXiQkR3Hledx00yqj0pned'
# Replace this endpoint secret with your endpoint's unique secret
# If you are testing with the CLI, find the secret by running 'stripe listen'
# If you are using an endpoint defined with the API or dashboard, look in your webhook settings
# at https://dashboard.stripe.com/webhooks
endpoint_secret = 'whsec_4f7ffef8aa2fff6f728882e3ecfc790a4ec6766bc2fc65f9c91e9fd31c0b42e8'

logging.basicConfig(level=logging.INFO)

@app.route('/', methods=['GET'])
def test():
    response = requests.get('http://user-service:8001/')
    print("Hello, world!")
    return response.json()


@app.route('/account', methods=['POST'])
def add_account():
    data = request.json
    shop_id = data.get('shop_id')
    try:
        new_account = dynamodb.add_shop_account(shop_id)
        if new_account is None:
            return jsonify({'status': False, 'message': 'Unable to create account.'}), 400
        return jsonify({'status': True, 'value': new_account}), 200
    except ClientError as e:
        print("Error adding user:", e)
        return jsonify({'status': False, 'message': 'Error'}), 500


@app.route('/account/<shop_id>', methods=['GET'])
# Function to get an account by UUID
def get_account(shop_id):
    try:
        account = dynamodb.get_account_json(shop_id)
        if account is None:
            return jsonify({'status': False, 'message': 'Unable to retrieve account.'}), 400
        return jsonify({'status': True, 'value': account}), 200
    except ClientError as e:
        print("Error getting user:", e)


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(data['total_price'] * 100),
            currency='chf',
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={
                'order_id': data['order_id'],
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data

    try:
        event = json.loads(payload)
    except json.decoder.JSONDecodeError as e:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return jsonify(success=False)
    if endpoint_secret:
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return jsonify(success=False)

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        order_id = payment_intent['metadata'].get('order_id', None)
        order_data = get_order(order_id)
        handle_payment_intent_succeeded(order_data)
        # Send confirmation mail
        #
        # Get mail from user from user-service
        # possible through the user id in orders
        # but currently orders are beeing reworked
        # first neccessary to finish that
        #user_id=order_data['user_id']
        #mail = get_user_mail(user_id)
        #send_order_confirmation("lukas.huber99@icloud.com", order_data)
        print('Payment for {} succeeded'.format(order_id))
    return jsonify(success=True)


#@app.route('/payment', methods=['PUT'])
def handle_payment_intent_succeeded(order_data):
    # Calculate subtotals for each shop
    shop_subtotals = {}
    for product in order_data['orders_fe']:
        product_owner = product['product_owner']
        price = product['price']
        quantity = product['quantity']

        if product_owner not in shop_subtotals:
            shop_subtotals[product_owner] = 0
        shop_subtotals[product_owner] += float(price) * int(quantity)

    # Create a charge and specify how the funds should be split
    for shop_id, amount in shop_subtotals.items():
        if dynamodb.shop_in_db(shop_id) is None:
            dynamodb.add_shop_account(shop_id)
        dynamodb.update_balance(shop_id, amount)
    return jsonify({'status': True, 'value': f"Transferred success"}), 201


def send_order_confirmation(email, order_details):
    mail = Mail(app)
    msg = Message('Order Confirmation')
    address = email
    msg.recipients.append(str(address))
    msg.body = f'Hello, your order has been confirmed. Details: {order_details}'
    mail.send(msg)
    return True


#@app.route('/test_product/<product_id>', methods=['GET'])
def get_shop_from_product(product_id):
    response = requests.get(f'http://inventory_management:8002/product/{product_id}')
    if response.status_code == 200:
        # Return the JSON response from the external service
        data = response.json()
        return data['value']['product_owner']
    else:
        return None

#@app.route('/mail/<user_id>', methods=['GET'])
def get_user_mail(user_id):
    response = requests.get(f'http://user-service:8001/users/{user_id}')
    logging.info(response)
    if response.status_code == 201:
        # Return the JSON response from the external service
        data = response.json()
        logging.info(data)
        return data['value']['email']
    else:
        return None


def get_order(order_id):
    response = requests.get(f"http://orders:8004/orders/{order_id}")
    response = {
        "order_id": "fdefe9fe-1a9c-48be-b9ac-e13e98788e0c",
        "orders": {
            "e96ff733-f85b-4d0a-a5ee-3900ea00050d": "7"
        },
        "orders_fe": [
            {
                "product_id": "e96ff733-f85b-4d0a-a5ee-3900ea00050d",
                "product_owner": "1324a686-c8b1-4c84-bbd6-17325209d78c6",
                "price": 7,
                "quantity": 7
            },
            {
                "product_id": "e55ff733-f85b-4d0a-a5ee-3900ea00050d",
                "product_owner": "1124a686-c8b1-4c84-bbd6-17325209d78c6",
                "price": 7,
                "quantity": 1
            },
            {
                "product_id": "e88ff733-f85b-4d0a-a5ee-3900ea00050d",
                "product_owner": "1324a686-c8b1-4c84-bbd6-17325209d78c6",
                "price": 7,
                "quantity": 2
            }
        ],
        "product_owners": {
            "e96ff733-f85b-4d0a-a5ee-3900ea00050d": "1324a686-c8b1-4c84-bbd6-17325209d78c6"
        },
        "total_price": 82.32,
        "user_id": "384172b4-3aa6-490e-bda5-e90d0dfccfab"
    }
    return response
    #if response.status_code == 201:
    # Return the JSON response from the external service
    #return jsonify(response.json()), 200
    #else:
    #   return None

