import boto3
import uuid
from botocore.exceptions import ClientError
import bcrypt
import logging
from app import utils, dynamodb_po, initialise_dynamo
from datetime import datetime

TABLE_NAME = 'OrdersManagement'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
db_order_management = initialise_dynamo.db_order_management

# Function to create orders table
def create_orders_table():
    """_summary_
    """
    try:
        response = db_order_management.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'order_id', 'KeyType': 'HASH'},
            ],
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'order_status', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[ 
                {
                    'IndexName': 'userIdIndx',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                },
                {
                    'IndexName': 'statusIndx',
                    'KeySchema': [
                        {'AttributeName': 'order_status', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                }
            ]
        )
        print("OrdersManagement table created:", response)
    except ClientError as e:
        print("Error creating OrdersManagement table:", e)


def delete_order_management_tables():
    """_summary_
    """
    try:
        db_order_management.delete_table(TableName=TABLE_NAME)
    except db_order_management.exceptions.ResourceNotFoundException:
        print("Table does not exist.")




# add item to the dynamodb
def add_item(user_id,product_id, quantity):
    """_summary_

    Args:
        user_id (_type_): _description_
        product_id (_type_): _description_
        quantity (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        # Generate UUID for the new user
        order_uuid = str(uuid.uuid4())

        #get product details from product service
        product_price, product_price_reduction, product_owner = utils.get_product_details(product_id)
    
        discounted_price = utils.calc_discounted_price(product_price, product_price_reduction)
        total_price = discounted_price*quantity
        status = 'unpaid'


        if quantity <= 0:
                return {'status': False, 'value': 'product quantity has to be at least 1!'}

        current_time = str(datetime.now())
        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                'order_id': {'S': f'{order_uuid}'},
                'user_id': {'S': user_id},
                'orders': {'M':  {product_id: {"N": str(quantity)}}}, 
                'product_owners': {'M':  {product_id: {"S": product_owner}}}, 
                'total_price': {'N': str(total_price)},
                'order_status': {'S': status},
                'execution_time': {'S': current_time},
            }
        )

        #add corresponding po orders in po orders db
        dynamodb_po.add_po_order(po_id = product_owner,order_id= order_uuid, user_id= user_id,product_id = product_id, quantity = quantity)

        print("Order added with UUID:", order_uuid)
        return get_order(order_uuid)
    except ClientError as e: 
        return str(e)

def get_order(order_uuid):
    """_summary_

    Args:
        order_uuid (_type_): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    try:
        response = db_order_management.get_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': f'{str(order_uuid)}'},
            }
        )
        item = response.get('Item')
        print('RESONSEE ITEMMM:', response)

        # If no order is found, return an error message
        if not item:
            raise ValueError('No order found with given ID') 

        order_info = utils.reformat_order_reponse(item)
        return order_info

    except ClientError as e:
        return str(e)
   


def get_all_orders():
    """_summary_

    Returns:
        _type_: _description_
    """
    try:
        response = db_order_management.scan(TableName=TABLE_NAME)
        return  utils.reformat_order_arr_reponse(response) 
       
    except ClientError as e:
        print("Error getting order:", e)



def update_order(order_id, product_id, quantity_change):
    """_summary_

    Args:
        order_id (_type_): _description_
        product_id (_type_): _description_
        quantity_change (_type_): _description_

    Raises:
        str: _description_

    Returns:
        _type_: _description_
    """
    try:
        #get current order values
        try:
            order = get_order(order_id)
        except ClientError as e:
            #print("Error getting order:", e)
            return str(e)

        orders_dict = order['orders']
        orders_po_dict = order['product_owners']
        total_price = float(order['total_price'])
        user_id = order['user_id']

       #get product details
        product_price, product_price_reduction, product_owner = utils.get_product_details(product_id)
        discounted_price_change = utils.calc_discounted_price(product_price, product_price_reduction)*quantity_change

        #To confirm if product needs to be updated in PO Orders, this is not the case if its deleted, or newly added
        po_order_update_flag = True
        #get po_order_id
        po_order = dynamodb_po.search_po_orders(product_owner=product_owner , order_id=order_id)
        if(po_order == 'Invalid Search'):
            count = 0
        else:
            count = 1

        #no corresponding po order found and new product
        if  count == 0 and (product_id not in orders_dict):
            #add corresponding po orders in po orders db
            dynamodb_po.add_po_order(product_owner,order_id, user_id,product_id , quantity_change)
            po_order_update_flag = False
        elif count == 0:
            return 'No corresponding po_order found '
        elif count > 1:
            return 'More than 1 po order was found, expected only 1'
        else:
            po_order_id = po_order['po_order_id']

        

        #check if product exists
        if product_id not in orders_dict:
            if quantity_change < 0:
                return {'status': False, 'value': 'product quantity cannot be less than 0 !'}
            
            #no corresponding po order found and new product
            if  count == 0 :
                #add corresponding po orders in po orders db
                dynamodb_po.add_po_order(product_owner,order_id, user_id,product_id , quantity_change)
                po_order_update_flag = False

            orders_dict[product_id] = quantity_change
            orders_po_dict[product_id] = product_owner

        else: 
            
            #modify po order db
            if count == 0:
                return 'No corresponding po_order found '
            elif count > 1:
                return 'More than 1 po order was found, expected only 1'
            else:
                po_order_id = po_order['po_order_id']

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
                del orders_po_dict[product_id]
                dynamodb_po.remove_po_product(po_order_id, product_id, discounted_price_change, total_quantity) 
                po_order_update_flag = False

            else:
                #update quantiy
                orders_dict[product_id] = float(orders_dict[product_id]) + float(quantity_change)

        #modify total price  
        total_price += discounted_price_change

        #update po order db
        if po_order_update_flag:
            dynamodb_po.update_po_order(po_order_id, product_id, quantity_change, discounted_price_change)

        # Dynamically build the update expression based on provided attributes
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "set "
        expression_attribute_values = {}

       #{"product_id1": 2, "product_id2":  2} --> {"product_id1": {"N": "2"}, "product_id2": {"N": "2"}}
        orders_exp = {}
        for key, value in orders_dict.items():
            orders_exp[key] = {"N": str(value)}
            orders_po_dict[key] = {"S": orders_po_dict[key]}


        update_expression += f"{'orders'} = :{'orders'},"
        expression_attribute_values[f":{'orders'}"] = {'M': orders_exp}

        update_expression += f"{'product_owners'} = :{'product_owners'},"
        expression_attribute_values[f":{'product_owners'}"] = {'M': orders_po_dict}

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
        raise str(e)

def update_status(order_id,status):
    """_summary_

    Args:
        order_id (_type_): _description_
        status (_type_): _description_

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        order_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        # Perform the delete operation
        response =  db_order_management.delete_item(
            TableName=TABLE_NAME,
            Key={
                'order_id': {'S': order_id},
            }
        )
        #delete corresponding orders from po_orders_table

        #get po_order_id
        po_orders = dynamodb_po.search_orders_by_orderid(order_id)
        count = int(po_orders['Count'])
        if count == 0:
            return 'Error Deleting: No corresponding po_order found '

        items = po_orders['Items']
        for item in items:
            po_order_id = item['po_order_id']
            dynamodb_po.delete_po_order(po_order_id)
        #return {'status': True, 'value': f'order with id {order_id} deleted successfully'}
        return response
    except :
        print(f"Error deleting")
        return False

def search_orders(user_id):
    """_summary_

    Args:
        user_id (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        #terms can include: user_id, product_id, status  #TODO add time
        response = db_order_management.query(
                    TableName=TABLE_NAME,
                    IndexName='userIdIndx',
                    KeyConditionExpression="user_id = :user_id",
                    ExpressionAttributeValues= {':user_id': {'S': user_id}}
                )
        return utils.reformat_order_arr_reponse(response)  

    except ClientError as e:
        print(f"Error deleting: {e}")
        return False


def search_orders_by_status(status):
    """_summary_

    Args:
        status (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        #terms can include: user_id, product_id, status  #TODO add time
        response = db_order_management.query(
                    TableName=TABLE_NAME,
                    IndexName='statusIndx',
                    KeyConditionExpression="order_status = :order_status",
                    ExpressionAttributeValues= {':order_status': {'S': status}}
                )
        return utils.reformat_order_arr_reponse(response)  

    except ClientError as e:
        print(f"Error deleting: {e}")
        return False


def search_orders_by_userid_and_status(user_id, status):
    """_summary_

    Args:
        user_id (_type_): _description_
        status (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        orders = search_orders(user_id)
        res = []
        for item in orders['Items']:
            if item['order_status'] == status :
                res.append(item)

        return  {"Count":len(res), "Items":res}

    except ClientError as e:
        print(f"Error searching: {e}")
        return False
  

