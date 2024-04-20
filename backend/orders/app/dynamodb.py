import boto3
import uuid
from botocore.exceptions import ClientError
import bcrypt
import logging
from app import utils
from datetime import datetime

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
def add_order(user_id,orders,total_price,execution_time,order_status):
    try:
        # Generate UUID for the new user
        order_uuid = str(uuid.uuid4())

        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                'order_id': {'S': f'{order_uuid}'},
                'user_id': {'S': user_id},
                'orders': {'M':  {"product_id1": {"N": "2"}, "product_id2": {"N": "2"}}}, # product ids
                'total_price': {'N': total_price},
                'execution_time': {'S': execution_time},
                'order_status': {'S': order_status},
                'product_owner': {'S': str(uuid.uuid4())}}
        )
        print("Order added with UUID:", order_uuid)
        return get_order(order_uuid)
    except ClientError as e: 
        print("Error adding user:", e)


# add item to the dynamodb
def add_item(user_id,product_id, quantity):
    try:
        # Generate UUID for the new user
        order_uuid = str(uuid.uuid4())

        #get product details from product service
        product_details = utils.get_product_details(product_id)
        product_price_reduction = float(product_details['product_price_reduction'])
        product_price = float(product_details['product_price'])
        product_owner = product_details['product_owner']

        discounted_price = utils.calc_discounted_price(product_price, product_price_reduction)
        total_price = discounted_price*quantity
        status = 'Processed'


        if quantity <= 0:
                return {'status': False, 'value': 'product quantity has to be at least 1!'}


        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                'order_id': {'S': f'{order_uuid}'},
                'user_id': {'S': user_id},
                'orders': {'M':  {product_id: {"N": str(quantity)}}}, # product ids
                'total_price': {'N': str(total_price)},
                'execution_time': {'S': ''},
                'order_status': {'S': status},
                'product_owner': {'S': product_owner},
            }
        )
        print("Order added with UUID:", order_uuid)
        return get_order(order_uuid)
    except ClientError as e: 
        return  {'status': False, 'value': f'error adding user {e} '}

def get_order(order_uuid):
    try:
        #TODO: handle no order id found case
        response = db_order_management.get_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': f'{str(order_uuid)}'},
            }
        )
        item = response.get('Item')
        order_info = utils.reformat_reponse(item)
        return order_info

    except ClientError as e:
        print("Error getting order:", e)
   


def get_all_orders():
    try:
        response = db_order_management.scan(TableName=TABLE_NAME)
        items = response.get('Items')
        final_res = []
        for item in items:
            final_res.append(utils.reformat_reponse(item))

        return  {"Count":response.get('Count'), "Items":final_res}
       
    except ClientError as e:
        print("Error getting order:", e)



def update_order(order_id, product_id, quantity_change):
    try:
        #get current order values
        order = get_order(order_id)
        orders_dict = order['orders']
        total_price = float(order['total_price'])

       #get product details
        product_details = utils.get_product_details(product_id)
        product_price_reduction = float(product_details['product_price_reduction'])
        product_price = float(product_details['product_price'])

        #check if product exists
        if product_id not in orders_dict:
            if quantity_change < 0:
                return {'status': False, 'value': 'product quantity cannot be less than 0 !'}

            orders_dict[product_id] = quantity_change
        else: 

            #modify quantity
            current_quantity = float(orders_dict[product_id])
            #quantity_change is negative if the user removes items from the cart
            #return an error if the quantitiy is less than zero after the subtraction
            total_quantity = current_quantity + quantity_change

            if total_quantity < 0 :
                return {'status': False, 'value': 'product quantity cannot be less than 0 !'}


            #if quantity is zero, remove product attributes from all arrays
            if total_quantity == 0:
                del orders_dict[product_id]
            else:
                #update quantiy
                orders_dict[product_id] = float(orders_dict[product_id]) + float(quantity_change)

        #modify total price  
        total_price += (utils.calc_discounted_price(product_price, product_price_reduction)*quantity_change)

        # Dynamically build the update expression based on provided attributes
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "set "
        expression_attribute_values = {}

       #{"product_id1": 2, "product_id2":  2} --> {"product_id1": {"N": "2"}, "product_id2": {"N": "2"}}
        orders_exp = {}
        for key, value in orders_dict.items():
            orders_exp[key] = {"N": str(value)}

        update_expression += f"{'orders'} = :{'orders'},"
        expression_attribute_values[f":{'orders'}"] = {'M': orders_exp}


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

def update_status(order_id,status):
    try:
        current_time = str(datetime.now())
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "set "
        expression_attribute_values = {}
        update_expression += f"{'execution_time'} = :{'execution_time'},"
        expression_attribute_values[f":{'execution_time'}"] = {'S': current_time}

        update_expression += f"{'order_status'} = :{'order_status'},"
        expression_attribute_values[f":{'order_status'}"] = {'S':status}

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

def search_orders(terms):
    try:
        #terms can include: user_id, product_id, status  #TODO add time
        search_expression = ""
        expression_attribute_values = {}
        start_flag = True
 
        for key, value in terms.items(): 
            if not start_flag:
                search_expression += ' AND '
            else:
                start_flag = False  

            search_expression += f"{key} = :{key},"
            expression_attribute_values[f":{key}"] = {'S': value}
            
            # Remove the trailing comma and space from expression
            search_expression = search_expression.rstrip(", ")


            # if key == 'user_id':
            #     search_expression += f"{'user_id'} = :{'user_id'},"
            #     expression_attribute_values[f":{'user_id'}"] = {'S': terms[key]}
            #     start_flag = False   

            # elif key == 'status':
               
            #     search_expression += f"{'status'} = :{'status'},"
            #     expression_attribute_values[f":{'status'}"] = {'S': terms[key]}

            # elif key == 'product_owner_id':
            #     if not start_flag:
            #         search_expression += 'AND'
            #     search_expression += f"{'product_owner_id'} = :{'product_owner_id'},"
            #     expression_attribute_values[f":{'product_owner_id'}"] = {'S': terms[key]}
            # else:
            #     return 'Invalid Search Term'
        #return f":search_expression: {search_expression} \n,expression_attribute_values:   {expression_attribute_values}"
        response = db_order_management.query(
                    TableName=TABLE_NAME,
                    KeyConditionExpression=search_expression,
                    ExpressionAttributeValues=expression_attribute_values
                )
        return response

    except ClientError as e:
        print(f"Error deleting: {e}")
        return False


