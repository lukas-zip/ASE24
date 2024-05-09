from botocore.exceptions import ClientError
from app import dynamodb
import requests
import json
from flask import jsonify, request
import stripe
import logging
from flask import Blueprint

# This is your test secret API key.
stripe.api_key = 'sk_test_51P3x1RL2VoulaBDdRpHDMZQCFlvnAmG1D1HRzjwnual8vUucfqdIRJiuMDGXOcVP5m6zwvaYPE6QzXiQkR3Hledx00yqj0pned'
# Replace this endpoint secret with your endpoint's unique secret
# If you are testing with the CLI, find the secret by running 'stripe listen'
# If you are using an endpoint defined with the API or dashboard, look in your webhook settings
# at https://dashboard.stripe.com/webhooks
endpoint_secret = 'whsec_4f7ffef8aa2fff6f728882e3ecfc790a4ec6766bc2fc65f9c91e9fd31c0b42e8'

route_blueprint = Blueprint('', __name__,)
logging.basicConfig(level=logging.INFO)

@route_blueprint.route('/', methods=['GET'])
def test():
    """
    A simple test route that confirms the server is operational.

    :return: A JSON response containing a status indicator and a test message, along with HTTP status code 200.
    """
    print("Hello, world!")
    return jsonify({'status': True, 'value': 'Test successful'}), 200


@route_blueprint.route('/account', methods=['POST'])
def add_account():
    """
    Creates a new account in the DynamoDB table using an API endpoint. Extracts 'shop_id' from the POST request JSON body.

    :return: JSON response containing the creation status and the new account ID if successful, or an error message if not.
    :raises ClientError: If there's a DynamoDB client error during account creation.
    """
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


@route_blueprint.route('/account/<shop_id>', methods=['GET'])
# Function to get an account by UUID
def get_account(shop_id):
    """
    Retrieves an account's details by shop_id from the DynamoDB table. Logs the account data and handles retrieval errors.

    :param shop_id: The unique identifier for the shop.
    :return: JSON response containing the account details if found, or an error message if not.
    :raises ClientError: If there's a DynamoDB client error during account retrieval.
    """
    try:
        account = dynamodb.get_account_json(shop_id)
        logging.info(account)
        if account is None:
            return jsonify({'status': False, 'message': 'Unable to retrieve account.'}), 400
        return jsonify({'status': True, 'value': account}), 200
    except ClientError as e:
        print("Error getting user:", e)


@route_blueprint.route('/create-payment-intent', methods=['POST'])
def create_payment():
    """
    Creates a Stripe PaymentIntent based on the total price and order ID received via POST request.

    :return: JSON response with the clientSecret of the PaymentIntent for client-side use, or an error message.
    :raises Exception: If there is an error during PaymentIntent creation.
    """
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


@route_blueprint.route('/webhook', methods=['POST'])
def webhook():
    """
    Handles incoming webhook events from Stripe, verifies the signature, processes the payment event, and
    updates order status if payment succeeds. Logs errors and events for diagnostics.

    :return: JSON response indicating success or failure based on the event handling.
    :raises stripe.error.SignatureVerificationError: If the signature verification of the webhook fails.
    :raises json.decoder.JSONDecodeError: If there is an error parsing the JSON payload from Stripe.
    """
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
    logging.info(event['type'])
    if event and event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        order_id = payment_intent['metadata'].get('order_id', None)
        order_data = get_order(order_id)
        handle_payment_intent_succeeded(order_data['value'], order_id)
        #sending out mails
        #user_id=order_data['user_id']
        #mail = get_user_mail(user_id)
        #send_order_confirmation(mail, order_id)
        print('Payment for {} succeeded'.format(order_id))
        create_invoice(order_id)
        update_order_payed(order_id)
    return jsonify(success=True)


def handle_payment_intent_succeeded(order_data, order_id):
    """
    Processes a successful payment by allocating the total payment across sub-orders based on shop subtotals,
    and updates each shop's balance. This function is invoked as part of the webhook handler for successful payments.

    :param order_data: The data pertaining to the order including items and quantities.
    :param order_id: The unique identifier for the order.
    :return: JSON response indicating the success of the funds transfer across sub-orders.
    """
    # Calculate subtotals for each shop
    shop_subtotals = {}
    for product in order_data['orders_fe']:
        product_owner = product['product_owner']
        price = product['final_price']
        quantity = product['quantity']

        if product_owner not in shop_subtotals:
            update_suborder_payed(order_id, product_owner)
            shop_subtotals[product_owner] = 0

        shop_subtotals[product_owner] += float(price) * int(quantity)

    # Create a charge and specify how the funds should be split
    for shop_id, amount in shop_subtotals.items():
        if dynamodb.shop_in_db(shop_id) is None:
            dynamodb.add_shop_account(shop_id)
        dynamodb.update_balance(shop_id, amount)
    return jsonify({'status': True, 'value': f"Transferred success"}), 201


def send_order_confirmation(email, order_id):
    """
    Sends an order confirmation email to the user using the Flask-Mail extension. This function is called after a successful
    order payment is processed.

    :param email: The recipient's email address.
    :param order_id: The unique identifier for the order.
    :return: True if the email is sent successfully.
    """
    from app import app  # Import here within the function
    from flask_mail import Mail, Message

    mail = Mail(app)
    msg = Message('Order Confirmation Claire')
    address = email
    msg.recipients.append(str(address))
    msg.body = f'Hello, your order has been confirmed. Order ID: {order_id}'
    mail.send(msg)
    return True



def get_shop_from_product(product_id):
    """
    Retrieves the shop owner of a product by querying an external inventory management service.

    :param product_id: The unique identifier for the product.
    :return: The shop owner if the product is found, None otherwise.
    """
    response = requests.get(f'http://inventory_management:8002/product/{product_id}')
    if response.status_code == 200:
        # Return the JSON response from the external service
        data = response.json()
        return data['value']['product_owner']
    else:
        return None


def get_user_mail(user_id):
    """
    Fetches a user's email by user_id from an external user service.

    :param user_id: The unique identifier for the user.
    :return: The user's email if found, None otherwise.
    """
    response = requests.get(f'http://user-service:8001/users/{user_id}')
    if response.status_code == 201:
        # Return the JSON response from the external service
        data = response.json()
        return data['value']['email']
    else:
        return None


def get_order(order_id):
    """
    Retrieves an order by its ID from an external orders service.

    :param order_id: The unique identifier for the order.
    :return: The order details if found, None otherwise.
    """
    response = requests.get(f"http://orders:8004/orders/{order_id}")
    if response.status_code == 200:
    #Return the JSON response from the external service
        return response.json()
    else:
       return None


def update_order_payed(order_id):
    """
    Updates the payment status of an order to 'paid' by contacting an external order management service.

    :param order_id: The unique identifier for the order whose status is to be updated.
    :return: True if the update is successful, False otherwise.
    """
    response = requests.get(f"http://orders:8004/orders/{order_id}/status/paid")
    if response.status_code == 200:
        return True
    else:
        return False


def create_invoice(order_id):
    """
    Generates an invoice for a completed order by interacting with an external order management service.

    :param order_id: The unique identifier for the order for which the invoice is created.
    :return: True if the invoice creation is successful, False otherwise.
    """
    response = requests.post(f"http://orders:8004/invoice/{order_id}")
    if response.status_code == 200:
        return True
    else:
        return False


def update_suborder_payed(order_id, product_owner_id):
    """
    Updates the payment status of a suborder to 'paid'. This function is called as part of the payment processing workflow.

    :param order_id: The unique identifier for the order.
    :param product_owner_id: The unique identifier for the product owner or shop.
    :return: True if the update is successful, False otherwise.
    """
    response = requests.get(f"http://orders:8004/orders/product/{order_id}/{product_owner_id}/paid")
    if response.status_code == 200:
        return True
    else:
        return False


