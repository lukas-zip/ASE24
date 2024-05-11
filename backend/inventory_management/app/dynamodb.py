import boto3
import uuid
from app import s3
from botocore.exceptions import ClientError
from io import BytesIO
from urllib.parse import quote_plus
import logging
import os

db_inventory_management = boto3.client(
    "dynamodb",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
    endpoint_url="http://localstack:4566"
)

# ------------------------------------------
# Product Database --> Dynamodb
# ------------------------------------------

# Function to create the profiles table
def create_product_table():
    
    try:
        # Check if the table already exists
        db_inventory_management.describe_table(TableName='Products')
        print("Products table already exists.")
    except db_inventory_management.exceptions.ResourceNotFoundException:
        # Table doesn't exist, so create it
        print("Creating Products table...")
        db_inventory_management.create_table(
            TableName='Products',
            KeySchema=[
                {
                    'AttributeName': 'product_id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'product_id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print("Products table created.")

def create_product_owner_index():
    try:
        response = db_inventory_management.update_table(
            TableName='Products',
            AttributeDefinitions=[
                {'AttributeName': 'product_owner', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': 'product_owner-index',
                        'KeySchema': [
                            {'AttributeName': 'product_owner', 'KeyType': 'HASH'}
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'  # Projection type can be adjusted based on your needs
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                }
            ]
        )
        print("Global secondary index created:", response)
    except ClientError as e:
        print("Error creating global secondary index:", e)

# for search
def create_gsi():
    try:
        response = db_inventory_management.update_table(
            TableName='Products',
            AttributeDefinitions=[
                {'AttributeName': 'product_category', 'AttributeType': 'S'},
                {'AttributeName': 'product_search_attributes', 'AttributeType': 'SS'}
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': {
                        'IndexName': 'product_category_index',
                        'KeySchema': [{'AttributeName': 'product_category', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                },
                {
                    'Create': {
                        'IndexName': 'product_search_attributes_index',
                        'KeySchema': [{'AttributeName': 'product_search_attributes', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                }
            ]
        )
        print("Global Secondary Indexes created:", response)
    except ClientError as e:
        print("Error creating Global Secondary Indexes:", e)

# Function to get all products belonging to a shop
def get_products_by_product_owner(product_owner):
    try:
        products = {}
        response = db_inventory_management.query(
            TableName='Products',
            IndexName='product_owner-index',
            KeyConditionExpression='product_owner = :product_owner',
            ExpressionAttributeValues={':product_owner': {'S': product_owner}}
        )

        # Iterate through items and construct product dictionary
        for item in response.get('Items', []):
            product_id = item['product_id']['S']
            product_info = {
                'product_id': product_id,  # Include product_id in product_info
                'product_owner': item.get('product_owner', {}).get('S', ''),
                'product_name': item.get('product_name', {}).get('S', ''),
                'product_picture': item.get('product_picture', {}).get('SS', ''),
                'product_description': item.get('product_description', {}).get('S', ''),
                'product_current_stock': item.get('product_current_stock', {}).get('N', ''),
                'product_should_stock': item.get('product_should_stock', {}).get('N', ''),
                'product_price': item.get('product_price', {}).get('N', ''),
                'product_price_reduction': item.get('product_price_reduction', {}).get('N', ''),
                'product_sale': item.get('product_sale', {}).get('BOOL', False),
                'product_category': item.get('product_category', {}).get('SS', ''),
                'product_search_attributes': item.get('product_search_attributes', {}).get('SS', ''),
                'product_reviews': item.get('product_reviews', {}).get('SS', ''),
                'product_bom': item.get('product_bom', {}).get('SS', ''),
                'product_assemblies': item.get('product_assemblies', {}).get('S', '')
            }
            products[product_id] = product_info

        # Paginate if necessary
        while 'LastEvaluatedKey' in response:
            response = db_inventory_management.query(
                TableName='Products',
                IndexName='product_owner-index',
                KeyConditionExpression='product_owner = :product_owner',
                ExpressionAttributeValues={':product_owner': {'S': product_owner}},
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            for item in response.get('Items', []):
                product_id = item['product_id']['S']
                product_info = {
                    'product_id': product_id,  # Include product_id in product_info
                    'product_owner': item.get('product_owner', {}).get('S', ''),
                    'product_name': item.get('product_name', {}).get('S', ''),
                    'product_picture': item.get('product_picture', {}).get('SS', ''),
                    'product_description': item.get('product_description', {}).get('S', ''),
                    'product_current_stock': item.get('product_current_stock', {}).get('N', ''),
                    'product_should_stock': item.get('product_should_stock', {}).get('N', ''),
                    'product_price': item.get('product_price', {}).get('N', ''),
                    'product_price_reduction': item.get('product_price_reduction', {}).get('N', ''),
                    'product_sale': item.get('product_sale', {}).get('BOOL', False),
                    'product_category': item.get('product_category', {}).get('SS', ''),
                    'product_search_attributes': item.get('product_search_attributes', {}).get('SS', ''),
                    'product_reviews': item.get('product_reviews', {}).get('SS', ''),
                    'product_bom': item.get('product_bom', {}).get('SS', ''),
                    'product_assemblies': item.get('product_assemblies', {}).get('S', '')
                }
                products[product_id] = product_info

        return products

    except ClientError as e:
        print("Error getting products by product owner:", e)
        return {}

# check for Item existance
def product_check(product_id):
    try:
        response = db_inventory_management.get_item(
            TableName='Products',
            Key={
                'product_id': {'S': product_id}
            }
        )
        item = response.get('Item')
        return item is not None
    except ClientError as e:
        print("Error checking product:", e)
        return False

def add_product(product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_search_attributes, product_reviews, product_bom, product_assemblies, product_picture):
    
    try:
        # Generate UUID for the new product
        product_uuid = str(uuid.uuid4())

        # Check if the product already exists
        existing_products = get_products_by_product_owner(product_owner)
        
        # Iterate over each existing product
        for existing_product_id, existing_product_info in existing_products.items():
            if existing_product_info['product_name'] == product_name:
                print(f"A product with the same name already exists for {product_owner}.")
                return 

        # if not isinstance(product_search_attributes, list):
        #     product_search_attributes = [product_search_attributes],

        # Put the new item into the table
        response = db_inventory_management.put_item(
            TableName='Products',
            Item={
                'product_id': {'S': product_uuid},  # Automatically generated UUID
                'product_owner': {'S': product_owner},
                'product_name': {'S': product_name},
                'product_picture': {'SS': product_picture},  # Store URL/path to the image
                'product_description': {'S': product_description},
                'product_current_stock': {'N': str(product_current_stock)},
                'product_should_stock': {'N': str(product_should_stock)},
                'product_price': {'N': str(product_price)},
                'product_price_reduction': {'N': str(product_price_reduction)},
                'product_sale': {'S': str(product_sale)},
                'product_category': {'SS': product_category},
                'product_search_attributes': {'SS': product_search_attributes},
                'product_reviews': {'SS': product_reviews},
                'product_bom': {'SS': product_bom}, # Stückliste
                'product_assemblies': {'S': str(product_assemblies)} # Baugruppe oder nicht
            }
        )
        print("Product added with UUID:", product_uuid)
    except ClientError as e:
        print("Error adding product:", e)


# delete product from table
def delete_product(product_id):
    table_name = 'Products'
    try:
        response = db_inventory_management.delete_item(
            TableName=table_name,
            Key={
                'product_id': {'S': product_id}
            }
        )

        response2 = s3.delete_object(product_id)

        print("Product got successfully deleted.")
        return True
    except Exception as e:
        print("Error deleting item.", e)
        return False

# getting a single product
def get_product(product_id):
    table_name = 'Products'
    try:
        response = db_inventory_management.get_item(
            TableName=table_name,
            Key={
                'product_id': {'S': product_id}
            }
        )
        item = response.get('Item')
        if item:
            product_info = {
                'product_assemblies': item.get('product_assemblies', {}).get('S', ''),
                'product_bom': item.get('product_bom', {}).get('SS', []),
                'product_category': item.get('product_category', {}).get('SS', []),
                'product_current_stock': item.get('product_current_stock', {}).get('N', ''),
                'product_description': item.get('product_description', {}).get('S', ''),
                'product_id': item.get('product_id', {}).get('S', ''),
                'product_name': item.get('product_name', {}).get('S', ''),
                'product_owner': item.get('product_owner', {}).get('S', ''),
                'product_picture': item.get('product_picture', {}).get('SS', []),
                'product_price': item.get('product_price', {}).get('N', ''),
                'product_price_reduction': item.get('product_price_reduction', {}).get('N', ''),
                'product_sale': item.get('product_sale', {}).get('BOOL', False),
                'product_search_attributes': item.get('product_search_attributes', {}).get('SS', []),
                'product_reviews': item.get('product_reviews', {}).get('SS', []),
                'product_should_stock': item.get('product_should_stock', {}).get('N', '')
            }
            return product_info
        else:
            print("Product not found.")
            return None
    except ClientError as e:
        print("Error getting product:", e)
        return None

#update product
def update_product(product_id, product_owner, updated_data):
    try:
        table_name = 'Products'

        # Check if the product exists
        if not product_check(product_id):
            print("Product does not exist.")
            return False
        
        # Check ownership
        product_info = get_product(product_id)
        if product_info['product_owner'] != product_owner:
            print("Provided product_owner does not match the current product_owner.")
            return False
        
        # Prepare UpdateExpression and ExpressionAttributeValues
        update_expression = "SET "
        expression_attribute_values = {}

        for key, value in updated_data.items():
            # Include only valid attributes for update
            if key in ['product_name', 'product_description', 'product_current_stock', 
                    'product_should_stock', 'product_price', 'product_price_reduction', 
                    'product_sale', 'product_category', 'product_search_attributes', 
                    'product_reviews', 'product_bom', 'product_assemblies', 'product_picture', 'product_sale']:
                update_expression += f"{key} = :{key}, "
                
                # Check if the value is numeric
                if key in ['product_current_stock', 'product_should_stock', 
                        'product_price', 'product_price_reduction']:
                    expression_attribute_values[f":{key}"] = {'N': str(value)}  # Use 'N' for numeric attributes
                elif key in ['product_bom', 'product_reviews', 'product_search_attributes', 'product_category', 'product_picture']:
                    expression_attribute_values[f":{key}"] = {'SS': value}
                elif key in ['product_sale']:
                    expression_attribute_values[f":{key}"] = {'BOOL': value}
                else:
                    expression_attribute_values[f":{key}"] = {'S': str(value)}  # Use 'S' for string attributes
        
        # Remove the trailing comma and space from the UpdateExpression
        update_expression = update_expression.rstrip(", ")
        
        logging.info(f"UpdateExpression: {update_expression}")
        logging.info(f"ExpressionAttributeValues: {expression_attribute_values}")

        # Perform the update operation
        response = db_inventory_management.update_item(
            TableName=table_name,
            Key={
                'product_id': {'S': product_id}
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        
        print("Product updated successfully.")
        return True
    except ClientError as e:
        print("Error updating product:", e)
        return False

def perform_sell(product_id, product_owner, ordered_items):
    try:
        table_name = 'Products'

        # Check if the product exists
        if not product_check(product_id):
            print("Product does not exist.")
            return False
        
        # Check ownership
        product_info = get_product(product_id) # get current product
        if product_info['product_owner'] != product_owner:
            print("Provided product_owner does not match the current product_owner.")
            return False
        
        # Check if there's enough stock available
        current_stock = int(product_info['product_current_stock'])
        if current_stock < ordered_items:
            print("Not enough stock available.")
            return False

        # Update the product's stock
        updated_stock = current_stock - ordered_items
        response = update_product(product_id, product_owner, {'product_current_stock': updated_stock})
        if not response:
            print("Failed to update product stock.")
            return False
        
        print("Product sold successfully.")
        return True
    except ClientError as e:
        print("Error updating product:", e)
        return False

def search_products_by_category(category_term):
    try:
        response = db_inventory_management.scan(
            TableName='Products'
        )
        items = response.get('Items', [])

        lowercase_category_term = category_term.lower()
        
        formatted_results = {}
        for item in items:
            product_id = item.get('product_id', {}).get('S')
            categories = [cate.lower() for cate in item.get('product_category', {}).get('SS', [])]

            if any(lowercase_category_term in cate for cate in categories):
                product = {
                    "product_assemblies": item.get('product_assemblies', {}).get('S'),
                    "product_bom": item.get('product_bom', {}).get('SS'),
                    "product_category": item.get('product_category', {}).get('SS'),
                    "product_current_stock": item.get('product_current_stock', {}).get('N', ''),
                    "product_description": item.get('product_description', {}).get('S'),
                    "product_id": product_id,
                    "product_name": item.get('product_name', {}).get('S'),
                    "product_owner": item.get('product_owner', {}).get('S'),
                    "product_picture": item.get('product_picture', {}).get('SS'),
                    "product_price": item.get('product_price', {}).get('N', ''),
                    "product_price_reduction": item.get('product_price_reduction', {}).get('N', ''),
                    "product_reviews": item.get('product_reviews', {}).get('SS'),
                    "product_sale": item.get('product_sale', {}).get('S') == 'True',
                    "product_search_attributes": item.get('product_search_attributes', {}).get('SS'),
                    "product_should_stock": item.get('product_should_stock', {}).get('N', '')
                }
                formatted_results[product_id] = product

        return formatted_results
    except ClientError as e:
        print("Error searching products by category:", e)
        return []

def search_products_by_attributes(attributes_term):
    try:
        response = db_inventory_management.scan(
            TableName='Products'
        )
        
        items = response.get('Items', [])

        lowercase_attributes_term = attributes_term.lower()

        formatted_results = {}
        for item in items:
            product_id = item.get('product_id', {}).get('S')
            attributes = [attr.lower() for attr in item.get('product_search_attributes', {}).get('SS', [])]
            
            if any(lowercase_attributes_term in attr for attr in attributes):
                product = {
                    "product_assemblies": item.get('product_assemblies', {}).get('S'),
                    "product_bom": item.get('product_bom', {}).get('SS'),
                    "product_category": item.get('product_category', {}).get('SS'),
                    "product_current_stock": item.get('product_current_stock', {}).get('N'),
                    "product_description": item.get('product_description', {}).get('S'),
                    "product_id": product_id,
                    "product_name": item.get('product_name', {}).get('S'),
                    "product_owner": item.get('product_owner', {}).get('S'),
                    "product_picture": item.get('product_picture', {}).get('SS'),
                    "product_price": item.get('product_price', {}).get('N'),
                    "product_price_reduction": item.get('product_price_reduction', {}).get('N'),
                    "product_reviews": item.get('product_reviews', {}).get('SS'),
                    "product_sale": item.get('product_sale', {}).get('S') == 'True',
                    "product_search_attributes": item.get('product_search_attributes', {}).get('SS'),
                    "product_should_stock": item.get('product_should_stock', {}).get('N')
                }
                formatted_results[product_id] = product

        return formatted_results
    except ClientError as e:
        print("Error searching products by attributes:", e)
        return []

def delete_product_table():
    try:
        db_inventory_management.delete_table(TableName='Products')
    except db_inventory_management.exceptions.ResourceNotFoundException:
        print("The Table could not be found.")