import boto3
import uuid
from botocore.exceptions import ClientError
import bcrypt
import logging
from app import utils
from datetime import datetime
from app import initialise_dynamo

TABLE_NAME = 'ProductOwnerOrdersManagement'
db_order_management = initialise_dynamo.db_order_management
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Function to create the profiles table
def create_product_owner_orders_table():
    try:
        response = db_order_management.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'po_order_id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'po_order_id', 'AttributeType': 'S'},
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'product_owner', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'POIndx',
                    'KeySchema': [
                        {
                            'AttributeName': 'product_owner',
                            'KeyType': 'HASH'   
                        }
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                },
                                {
                    'IndexName': 'OrderIDIndx',
                    'KeySchema': [
                        {
                            'AttributeName': 'order_id',
                            'KeyType': 'HASH'   
                        }                      
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
                
            ]
        )
        print("PO OrdersManagement table created:", response)
    except ClientError as e:
        print("Error creating PO OrdersManagement table:", e)



def get_po_order(po_order_id):
    try:
        #TODO: handle no order id found case
        response = db_order_management.get_item(
            TableName=TABLE_NAME,
            Key={
                'po_order_id': {'S': po_order_id}
                }
            
        )
        item = response.get('Item')
        order_info = utils.reformat_po_order_reponse(item)
        return order_info

    except ClientError as e:
        print("Error getting po order:", e)
   

def get_all_po_orders():
    try:
        response = db_order_management.scan(TableName=TABLE_NAME)
        return  utils.reformat_po_order_arr_reponse(response)  
       
    except ClientError as e:
        print("Error getting po order:", e)


def delete_po_order(po_order_id):
    try:
        # Perform the delete operation
        response =  db_order_management.delete_item(
            TableName=TABLE_NAME,
            Key={
                'po_order_id': {'S': po_order_id},
            }
        )
        #return {'status': True, 'value': f'order with id {order_id} deleted successfully'}
        return response
    except ClientError as e:
        print(f"Error deleting: {e}")
        return False

# add order to the dynamodb
def add_po_order(po_id,order_id, user_id,product_id = None, quantity = None):
    try:

        # Generate UUID for the new user
        po_order_uuid = str(uuid.uuid4())

        orders = {}
        total_price = 0
        current_time = str(datetime.now())

        if product_id is not None:
            orders = {product_id: {"N": str(quantity)}}
            product_price, product_price_reduction, product_owner = utils.get_product_details(product_id)
            total_price = utils.calc_discounted_price(product_price, product_price_reduction)

        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                'po_order_id': {'S': f'{po_order_uuid}'},
                'order_id': {'S': f'{order_id}'},
                'product_owner': {'S': f'{po_id}'},
                'user_id': {'S': user_id},
                'orders': {'M': orders}, # product ids
                'total_price': {'N': str(total_price)},
                'execution_time': {'S': current_time},
                'order_status': {'S': 'processed'}
            }
        )
        print("PO order added with UUID:", po_order_uuid)
        return get_po_order(po_order_uuid)

    except ClientError as e: 
        print("Error adding user:", e)



def get_po_order(po_order_id):
    try:
        #TODO: handle no order id found case
        response = db_order_management.get_item(
            TableName=TABLE_NAME,
            Key={
                'po_order_id': {'S': po_order_id},
            }
        )
        item = response.get('Item')
        
        order_info = utils.reformat_po_order_reponse(item)
        return order_info

    except ClientError as e:
        print("Error getting order:", e)


def update_po_status(product_owner, order_id, status):
    try:
        #get po_order_id
        po_order = search_po_orders(product_owner=product_owner , order_id=order_id)
        # count = int(po_order['Count'])
        # if count == 0:
        #     return 'Error Updating Status: No corresponding po_order found'
        # elif count > 1:
        #     return 'Error Updating Status: more than 1 po_order found'
        #items = po_order['Items']
        #print('PO Orderrr',po_order)
        if po_order == 'Invalid Search':
            return 'No PO Order Found'
        po_order_id = po_order['po_order_id']


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
                'po_order_id': {'S': po_order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        print(f"order {po_order_id} status updated successfully.")
        return get_po_order(po_order_id)

    except ClientError as e:
        print(f"Error updating: {e}")
        raise e




def update_po_order(po_order_id, product_id, total_quantity, product_discounted_price_change):
    try:
        #get current order values
        order = get_po_order(po_order_id)
        orders_dict = order['orders']
        total_price = float(order['total_price'])

        #modify total price  
        total_price += product_discounted_price_change
        orders_dict[product_id] = total_quantity

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
                'po_order_id': {'S': po_order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        print(f"order {po_order_id} updated successfully.")
        return get_po_order(po_order_id)

    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


def remove_po_product(po_order_id, product_id, product_discounted_price_change, total_quantity):
    try:
        #get current order values
        order = get_po_order(po_order_id)
        orders_dict = order['orders']
        total_price = float(order['total_price'])

        #modify total price  
        total_price += product_discounted_price_change
        orders_dict[product_id] = total_quantity

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
                'po_order_id': {'S': po_order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        print(f"order {po_order_id} updated successfully.")
        return get_po_order(po_order_id)

    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


def search_orders_by_po(product_owner):
    try:
        response = db_order_management.query(
                    TableName=TABLE_NAME,
                    IndexName='POIndx',
                    KeyConditionExpression="product_owner = :product_owner",
                    ExpressionAttributeValues= {':product_owner': {'S': product_owner}}

                )
        return utils.reformat_po_order_arr_reponse(response) 

    except ClientError as e:
        print(f"Error searching: {e}")
        return False


def search_orders_by_orderid(order_id):
    try:
        response = db_order_management.query(
                    TableName=TABLE_NAME,
                    IndexName='OrderIDIndx',
                    KeyConditionExpression="order_id = :order_id",
                    ExpressionAttributeValues= {':order_id': {'S': order_id}}

                )
      #  if response == False:
        #return (f"Error searching PO DB search exp {search_expression}, exp attribute {expression_attribute_values}" )
        return utils.reformat_po_order_arr_reponse(response) 

    except ClientError as e:
        print(f"Error searching: {e}")
        return False


def search_po_orders(product_owner, order_id):
    search_orderid = search_orders_by_orderid(order_id)
    search_po = search_orders_by_po(product_owner)

    if search_orderid['Count'] == 0 or search_po['Count'] == 0 :
        return 'Invalid Search'
    
    #Look for overlapping results
    for po_order in search_orderid['Items']:
        if po_order in search_po['Items']:
            return po_order
    return 'Invalid Search'

    