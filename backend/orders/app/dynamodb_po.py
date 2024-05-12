import logging
import uuid
from datetime import datetime

import bcrypt
import boto3
from botocore.exceptions import ClientError

from app import initialise_dynamo, utils

TABLE_NAME = "ProductOwnerOrdersManagement"
db_order_management = initialise_dynamo.db_order_management
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Function to create the profiles table
def create_product_owner_orders_table():
    """Creates PO DynamoDB orders table"""
    try:
        response = db_order_management.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "po_order_id", "KeyType": "HASH"}],
            AttributeDefinitions=[
                {"AttributeName": "po_order_id", "AttributeType": "S"},
                {"AttributeName": "order_id", "AttributeType": "S"},
                {"AttributeName": "product_owner", "AttributeType": "S"},
                {"AttributeName": "order_status", "AttributeType": "S"},
                {"AttributeName": "user_id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "POIndx",
                    "KeySchema": [
                        {"AttributeName": "product_owner", "KeyType": "HASH"}
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "OrderStatusIndx",
                    "KeySchema": [{"AttributeName": "order_status", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "OrderIDIndx",
                    "KeySchema": [{"AttributeName": "order_id", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
                {
                    "IndexName": "UserIDIndx",
                    "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5,
                    },
                },
            ],
        )
        print("PO OrdersManagement table created:", response)
    except ClientError as e:
        print("Error creating PO OrdersManagement table:", e)


def delete_po_order_management_tables():
    """Delete PO orders table"""
    try:
        db_order_management.delete_table(TableName=TABLE_NAME)
    except db_order_management.exceptions.ResourceNotFoundException:
        print("Table does not exist.")


def get_po_order(po_order_id):
    """Fetches PO order from the table by its ID

    Args:
        po_order_id (string): Product Owner ID

    Returns:
        json: corresponding PO order
    """
    try:
        response = db_order_management.get_item(
            TableName=TABLE_NAME, Key={"po_order_id": {"S": po_order_id}}
        )
        item = response.get("Item")
        order_info = utils.reformat_po_order_reponse(item)
        return order_info

    except ClientError as e:
        print("Error getting po order:", e)


def get_all_po_orders():
    """Fetches all PO orders, used for debugging

    Returns:
        json: All PO orders in the database
    """
    try:
        response = db_order_management.scan(TableName=TABLE_NAME)
        return utils.reformat_po_order_arr_reponse(response)

    except ClientError as e:
        print("Error getting po order:", e)


def delete_po_order(po_order_id):
    """Deletes PO order from the table by ID

    Args:
        po_order_id (string): Product Owner ID

    Returns:
        : table response if successful, error if not
    """
    try:
        # Perform the delete operation
        response = db_order_management.delete_item(
            TableName=TABLE_NAME,
            Key={
                "po_order_id": {"S": po_order_id},
            },
        )
        return response
    except ClientError as e:
        print(f"Error deleting: {e}")
        return False


# add order to the dynamodb
def add_po_order(po_id, order_id, user_id, product_id=None, quantity=None):
    """Creates a new PO order with the passed product and its quantity

    Args:
        po_id (string): Product Owner ID
        order_id (string): Order ID
        user_id (string): User ID
        product_id (string, optional): Product ID. Defaults to None.
        quantity (integer, optional): Product Quantity . Defaults to None.

    Returns:
        json: PO order json
    """
    try:

        # Generate UUID for the new user
        po_order_uuid = str(uuid.uuid4())

        orders = {}
        total_price = 0
        current_time = str(datetime.now())

        if product_id is not None:
            orders = {product_id: {"N": str(quantity)}}
            product_price, product_price_reduction, product_owner = (
                utils.get_product_details(product_id)
            )
            total_price = utils.calc_discounted_price(
                product_price, product_price_reduction
            ) * float(quantity)

        # Put the new item into the table
        db_order_management.put_item(
            TableName=TABLE_NAME,
            Item={
                "po_order_id": {"S": f"{po_order_uuid}"},
                "order_id": {"S": f"{order_id}"},
                "product_owner": {"S": f"{po_id}"},
                "user_id": {"S": user_id},
                "orders": {"M": orders},  # product ids
                "total_price": {"N": str(total_price)},
                "execution_time": {"S": current_time},
                "order_status": {"S": "unpaid"},
            },
        )
        print("PO order added with UUID:", po_order_uuid)
        return get_po_order(po_order_uuid)

    except ClientError as e:
        print("Error adding user:", e)


def get_po_order(po_order_id):
    """Fetches PO Order by ID

    Args:
        po_order_id (string): Product Owner ID

    Returns:
        json:  PO order json
    """
    try:
        # TODO: handle no order id found case
        response = db_order_management.get_item(
            TableName=TABLE_NAME,
            Key={
                "po_order_id": {"S": po_order_id},
            },
        )
        item = response.get("Item")

        order_info = utils.reformat_po_order_reponse(item)
        return order_info

    except ClientError as e:
        print("Error getting order:", e)


def update_po_status(product_owner, order_id, status):
    """Updates PO order status from unpaid to paid or vice versa

    Args:
        product_owner (string): product owner ID
        order_id (string): order ID
        status (string): order status (paid/unpaid)

    Raises:
        e: error

    Returns:
        json:  PO order json
    """
    try:
        # get po_order_id
        po_order = search_po_orders(product_owner=product_owner, order_id=order_id)
        if po_order == "Invalid Search":
            return "No PO Order Found"
        po_order_id = po_order["po_order_id"]

        current_time = str(datetime.now())
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "set "
        expression_attribute_values = {}
        update_expression += f"{'execution_time'} = :{'execution_time'},"
        expression_attribute_values[f":{'execution_time'}"] = {"S": current_time}

        update_expression += f"{'order_status'} = :{'order_status'},"
        expression_attribute_values[f":{'order_status'}"] = {"S": status}

        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")

        # Execute the update operation
        db_order_management.update_item(
            TableName=TABLE_NAME,
            Key={
                "po_order_id": {"S": po_order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        print(f"order {po_order_id} status updated successfully.")
        return get_po_order(po_order_id)

    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


def update_po_order(
    po_order_id, product_id, quantity_change, total_discounted_price_change
):
    """Adds/Removes PO orders, and updates total price

    Args:
        po_order_id (string): Product Owner ID
        product_id (string): Product ID
        quantity_change : Product quantity (negative if removed, positive if added)
        total_discounted_price_change : change in price

    Raises:
        e: error

    Returns:
        json: PO order json
    """
    try:
        # get current order values
        order = get_po_order(po_order_id)
        orders_dict = order["orders"]
        total_price = float(order["total_price"])

        # modify total price
        total_price += float(total_discounted_price_change)
        if product_id not in orders_dict.keys():
            orders_dict[product_id] = 0
        orders_dict[product_id] = float(orders_dict[product_id]) + float(
            quantity_change
        )

        # Dynamically build the update expression based on provided attributes
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "set "
        expression_attribute_values = {}

        # {"product_id1": 2, "product_id2":  2} --> {"product_id1": {"N": "2"}, "product_id2": {"N": "2"}}
        orders_exp = {}
        for key, value in orders_dict.items():
            orders_exp[key] = {"N": str(value)}

        update_expression += f"{'orders'} = :{'orders'},"
        expression_attribute_values[f":{'orders'}"] = {"M": orders_exp}

        update_expression += f"{'total_price'} = :{'total_price'},"
        expression_attribute_values[f":{'total_price'}"] = {"N": str(total_price)}

        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")

        # Execute the update operation
        db_order_management.update_item(
            TableName=TABLE_NAME,
            Key={
                "po_order_id": {"S": po_order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        print(f"order {po_order_id} updated successfully.")
        return get_po_order(po_order_id)

    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


def remove_po_product(
    po_order_id, product_id, product_discounted_price_change, total_quantity
):
    """Removes product from  PO order

    Args:
        po_order_id (string): Product Owner ID
        product_id (string): Product ID
        product_discounted_price_change : product price after discount
        total_quantity : quantity removed

    Raises:
        e: error

    Returns:
        json : PO order json
    """
    try:
        # get current order values
        order = get_po_order(po_order_id)
        orders_dict = order["orders"]
        total_price = float(order["total_price"])

        # modify total price
        total_price += product_discounted_price_change
        orders_dict[product_id] = total_quantity
        # remove product from PO order
        del orders_dict[product_id]

        # Dynamically build the update expression based on provided attributes
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "set "
        expression_attribute_values = {}

        # {"product_id1": 2, "product_id2":  2} --> {"product_id1": {"N": "2"}, "product_id2": {"N": "2"}}
        orders_exp = {}
        for key, value in orders_dict.items():
            orders_exp[key] = {"N": str(value)}

        update_expression += f"{'orders'} = :{'orders'},"
        expression_attribute_values[f":{'orders'}"] = {"M": orders_exp}

        update_expression += f"{'total_price'} = :{'total_price'},"
        expression_attribute_values[f":{'total_price'}"] = {"N": str(total_price)}

        # Remove the trailing comma and space from the update expression
        update_expression = update_expression.rstrip(", ")

        # Execute the update operation
        db_order_management.update_item(
            TableName=TABLE_NAME,
            Key={
                "po_order_id": {"S": po_order_id},
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        print(f"order {po_order_id} updated successfully.")
        return get_po_order(po_order_id)

    except ClientError as e:
        print(f"Error updating: {e}")
        raise e


def search_orders_by_po(product_owner):
    """Searches PO orders according to product owner

    Args:
        product_owner (string): Product owner name

    Returns:
        json: Array of product owner orders jsons that match the search criteria
    """
    try:
        response = db_order_management.query(
            TableName=TABLE_NAME,
            IndexName="POIndx",
            KeyConditionExpression="product_owner = :product_owner",
            ExpressionAttributeValues={":product_owner": {"S": product_owner}},
        )
        return utils.reformat_po_order_arr_reponse(response)

    except ClientError as e:
        print(f"Error searching: {e}")
        return False


def search_orders_by_orderid(order_id):
    """Searches PO orders according to user order id

    Args:
        order_id (string): User order id

    Returns:
        json: Array of product owner jsons that match the search criteria
    """
    try:
        response = db_order_management.query(
            TableName=TABLE_NAME,
            IndexName="OrderIDIndx",
            KeyConditionExpression="order_id = :order_id",
            ExpressionAttributeValues={":order_id": {"S": order_id}},
        )
        return utils.reformat_po_order_arr_reponse(response)

    except ClientError as e:
        print(f"Error searching: {e}")
        return False


def search_po_orders(product_owner, order_id):
    """Searches PO orders according to user order id and product owner name

    Args:
        product_owner (string): Product Owner name
        order_id (string): Order ID

    Returns:
        json: Array of product owner jsons that match the search criteria
    """
    search_orderid = search_orders_by_orderid(order_id)
    search_po = search_orders_by_po(product_owner)

    if search_orderid["Count"] == 0 or search_po["Count"] == 0:
        return "Invalid Search"

    # Look for overlapping results
    for po_order in search_orderid["Items"]:
        if po_order in search_po["Items"]:
            return po_order
    return "Invalid Search"


def search_po_orders_by_status(order_status):
    """Searches PO orders according to  order status

    Args:
        order_status (string): PO order status

    Returns:
        json: Array of product owner jsons that match the search criteria
    """
    try:
        response = db_order_management.query(
            TableName=TABLE_NAME,
            IndexName="OrderStatusIndx",
            KeyConditionExpression="order_status = :order_status ",
            ExpressionAttributeValues={":order_status": {"S": order_status}},
        )
        return utils.reformat_po_order_arr_reponse(response)

    except ClientError as e:
        print(f"Error searching: {e}")
        return False


def search_po_orders_by_userid(user_id):
    """Searches PO orders according to  user ID

    Args:
        user_id (string): User ID

    Returns:
        json: Array of product owner jsons that match the search criteria
    """
    try:
        response = db_order_management.query(
            TableName=TABLE_NAME,
            IndexName="UserIDIndx",
            KeyConditionExpression="user_id = :user_id ",
            ExpressionAttributeValues={":user_id": {"S": user_id}},
        )
        return utils.reformat_po_order_arr_reponse(response)

    except ClientError as e:
        print(f"Error searching: {e}")
        return False


def search_orders_by_userid_and_status(user_id, status):
    """Searches PO orders according to  user ID and PO order status

    Args:
        user_id (string): User ID
        status (string): PO order status

    Returns:
        json: Array of product owner jsons that match the search criteria
    """
    try:
        orders = search_po_orders_by_userid(user_id)
        res = []
        for item in orders["Items"]:
            if item["order_status"] == status:
                res.append(item)

        return {"Count": len(res), "Items": res}

    except ClientError as e:
        print(f"Error searching: {e}")
        return False


def search_orders_by_po_id_and_status(po_id, status):
    """Searches PO orders according to PO ID and PO order status

    Args:
        po_id (string): Product Owner name/ID
        status (string): PO order status

    Returns:
        json: Array of product owner jsons that match the search criteria
    """
    try:
        orders = search_orders_by_po(po_id)
        res = []
        for item in orders["Items"]:
            if item["order_status"] == status:
                res.append(item)

        return {"Count": len(res), "Items": res}

    except ClientError as e:
        print(f"Error searching: {e}")
        return False
