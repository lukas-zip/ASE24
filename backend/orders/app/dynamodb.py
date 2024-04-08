import boto3
import uuid
from botocore.exceptions import ClientError
import bcrypt
import logging
from app import utils

TABLE_NAME = 'OrdersManagement'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

db_order_management = boto3.client(
    "dynamodb",
    aws_access_key_id="test",  # Dummy Access Key for LocalStack
    aws_secret_access_key="test",  # Dummy Secret Key for LocalStack
    region_name="us-east-1",  # or your LocalStack configuration's region
    endpoint_url="http://localstack:4566"  # URL for LocalStack
)
s3_client = boto3.client(
    "s3",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)

# Create S3 bucket on LocalStack
def create_s3_bucket():
    try:
        bucket_name = 'orders'
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


# Function to create the profiles table
def create_orders_table():
    try:
        response = db_order_management.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
        )
        print("OrdersManagement table created:", response)
    except ClientError as e:
        print("Error creating OrdersManagement table:", e)


# add order to the dynamodb
def add_order(username,orders,prices,total_price,execution_time,status,quantities):
    try:
        # Generate UUID for the new user
        order_uuid = str(uuid.uuid4())

        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                'order_id': {'S': f'{order_uuid}'},
                'username': {'S': username},
                'orders': {'SS':  orders}, # product ids
                'quantities': {'NS':  quantities}, 
                'total_price': {'N': total_price},
                'execution_time': {'S': execution_time},
                'status': {'S': status}
            }
        )
        print("Order added with UUID:", order_uuid)
        return get_order(order_uuid)
    except ClientError as e: 
        print("Error adding user:", e)


# add item to the dynamodb
def add_item(username,product_id, quantity, product_price, product_price_reduction):
    try:
        # Generate UUID for the new user
        order_uuid = str(uuid.uuid4())

        #get product details from product service
        #product_details = utils.get_product_details(product_id)

        orders = []
        quantities = []

        orders.append(product_id)
        discounted_price = utils.calc_discounted_price(product_price, product_price_reduction)
        quantities.append(str(quantity))
        
        total_price = discounted_price*quantity
        status = 'In Progress'

        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                'order_id': {'S': f'{order_uuid}'},
                'username': {'S': username},
                'orders': {'SS':  orders}, # product ids
                'quantities': {'NS':  quantities}, 
                'total_price': {'N': str(total_price)},
                'execution_time': {'S': ''},
                'status': {'S': status}
            }
        )
        print("Order added with UUID:", order_uuid)
        return get_order(order_uuid)
    except ClientError as e: 
        return  {'status': False, 'value': f'error adding user {e} '}

def get_order(order_uuid):
    try:
        response = db_order_management.get_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': f'{str(order_uuid)}'},
            }
        )
        return response
    except ClientError as e:
        print("Error getting order:", e)
   


def get_all_orders():
    try:
        response = db_order_management.scan(TableName=TABLE_NAME)
        return response
    except ClientError as e:
        print("Error getting order:", e)



def update_order(order_id, product_id, quantity_change, product_price, discount):
    try:
        #get current order values
        order = get_order(order_id)

        orders_arr = order['Item']['orders']['SS']

        quantities_arr = (order['Item']['quantities']['NS'])
        quantities_arr = list(map(int, quantities_arr))

        total_price = float(order['Item']['total_price']['N'])

       #get product details
        # product_details = utils.get_product_details(orders)
        # discount = product_details.product_price_reduction
        # product_price = product_details.product_price

        #check if product exists
        if product_id not in orders_arr: 
            if quantity_change < 0:
                return {'status': False, 'value': 'product quantity cannot be less than 0 !'}

            
            orders_arr.append(product_id)
            quantities_arr.append(quantity_change)

        else: 
            #get product id index
            product_index = orders_arr.index(product_id)

            #modify quantity
            current_quantity = quantities_arr[product_index]
            
            #quantity_change is negative if the user removes items from the cart
            #return an error if the quantitiy is less than zero after the subtraction
            total_quantity = current_quantity + quantity_change
            if total_quantity < 0 :
                return {'status': False, 'value': 'product quantity cannot be less than 0 !'}


            #if quantity is zero, remove product attributes from all arrays
            if total_quantity == 0:
                del orders_arr[product_index]
                del quantities_arr[product_index] 
            else:
                #update quantiy
                quantities_arr[product_index] = str(total_quantity)

        #modify total price  
        total_price += (utils.calc_discounted_price(product_price, discount)*quantity_change)

        #convert lists back to string lists
        quantities_arr = list(map(str, quantities_arr))

        # Dynamically build the update expression based on provided attributes
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "set "
        expression_attribute_values = {}
        update_expression += f"{'orders'} = :{'orders'},"
        expression_attribute_values[f":{'orders'}"] = {'SS': orders_arr}

        update_expression += f"{'quantities'} = :{'quantities'},"
        expression_attribute_values[f":{'quantities'}"] = {'NS': quantities_arr}

        update_expression += f"{'total_price'} = :{'total_price'},"
        expression_attribute_values[f":{'total_price'}"] = {'N': str(total_price)}

        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")

        # Execute the update operation
        db_order_management.update_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        print(f"order {order_id} updated successfully.")
        return get_order(order_id)

    except ClientError as e:
        print(f"Error updating: {e}")
        raise e

def delete_order(order_id):
    try:
        # Perform the delete operation
        response =  db_order_management.delete_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': order_id},
            }
        )
        #return {'status': True, 'value': f'order with id {order_id} deleted successfully'}
        return response
    except ClientError as e:
        print(f"Error deleting: {e}")
        return False
