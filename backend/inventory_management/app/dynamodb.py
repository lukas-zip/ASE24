import boto3
import uuid
from app import s3
from botocore.exceptions import ClientError
from io import BytesIO
from urllib.parse import quote_plus

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
                }
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
                'product_name': item.get('product_name', {}).get('S', ''),
                'product_picture': item.get('product_picture', {}).get('S', ''),
                'product_description': item.get('product_description', {}).get('S', ''),
                'product_current_stock': item.get('product_current_stock', {}).get('N', ''),
                'product_should_stock': item.get('product_should_stock', {}).get('N', ''),
                'product_price': item.get('product_price', {}).get('N', ''),
                'product_price_reduction': item.get('product_price_reduction', {}).get('N', ''),
                'product_sale': item.get('product_sale', {}).get('BOOL', False),
                'product_category': item.get('product_category', {}).get('S', ''),
                'product_search_attributes': item.get('product_search_attributes', {}).get('S', ''),
                'product_reviews': item.get('product_reviews', {}).get('S', ''),
                'product_bom': item.get('product_bom', {}).get('S', ''),
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
                    'product_name': item.get('product_name', {}).get('S', ''),
                    'product_picture': item.get('product_picture', {}).get('S', ''),
                    'product_description': item.get('product_description', {}).get('S', ''),
                    'product_current_stock': item.get('product_current_stock', {}).get('N', ''),
                    'product_should_stock': item.get('product_should_stock', {}).get('N', ''),
                    'product_price': item.get('product_price', {}).get('N', ''),
                    'product_price_reduction': item.get('product_price_reduction', {}).get('N', ''),
                    'product_sale': item.get('product_sale', {}).get('BOOL', False),
                    'product_category': item.get('product_category', {}).get('S', ''),
                    'product_search_attributes': item.get('product_search_attributes', {}).get('S', ''),
                    'product_reviews': item.get('product_reviews', {}).get('S', ''),
                    'product_bom': item.get('product_bom', {}).get('S', ''),
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

def add_product(product_owner, product_name, product_description, product_current_stock, product_should_stock, product_price, product_price_reduction, product_sale, product_category, product_search_attributes, product_reviews, product_bom, product_assemblies, image_file):
    
    try:
        # Generate UUID for the new product
        product_uuid = str(uuid.uuid4())

        # Put picture into S3
        bucket_name = 'productpictures'
        object_key = f'{product_uuid}.jpg'  # Use UUID as object key

        # Convert bytes object to file-like object
        image_stream = BytesIO(image_file.read())

        try:
            # Upload the image file to S3
            s3response = s3.upload_fileobj(image_stream, bucket_name, object_key)
            print("Product picture added with UUID:", product_uuid)
        except ClientError as e:
            print("Error uploading product picture to S3:", e)
            return
        
        # Construct the URL/path to the uploaded image
        s3_base_url = f'http://localhost:4566/{bucket_name}/' # Der Link ist derzeit auf Local angepasst
        image_url = s3_base_url + quote_plus(object_key)

        # Check if the product already exists
        existing_products = get_products_by_product_owner(product_owner)
        
        # Iterate over each existing product
        for existing_product_id, existing_product_info in existing_products.items():
            if existing_product_info['product_name'] == product_name:
                print(f"A product with the same name already exists for {product_owner}.")
                return 

        # Put the new item into the table
        response = db_inventory_management.put_item(
            TableName='Products',
            Item={
                'product_id': {'S': product_uuid},  # Automatically generated UUID
                'product_owner': {'S': product_owner},
                'product_name': {'S': product_name},
                'product_picture': {'S': image_url},  # Store URL/path to the image
                'product_description': {'S': product_description},
                'product_current_stock': {'N': str(product_current_stock)},
                'product_should_stock': {'N': str(product_should_stock)},
                'product_price': {'N': str(product_price)},
                'product_price_reduction': {'N': str(product_price_reduction)},
                'product_sale': {'S': str(product_sale)},
                'product_category': {'S': str(product_category)},
                'product_search_attributes': {'S': str(product_search_attributes)},
                'product_reviews': {'S': str(product_reviews)},
                'product_bom': {'S': str(product_bom)}, # Stückliste
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
                'product_id': item.get('product_id', {}).get('S', ''),
                'product_owner': item.get('product_owner', {}).get('S', ''),
                'product_name': item.get('product_name', {}).get('S', ''),
                'product_picture': item.get('product_picture', {}).get('S', ''),
                'product_description': item.get('product_description', {}).get('S', ''),
                'product_current_stock': item.get('product_current_stock', {}).get('N', ''),
                'product_should_stock': item.get('product_should_stock', {}).get('N', ''),
                'product_price': item.get('product_price', {}).get('N', ''),
                'product_price_reduction': item.get('product_price_reduction', {}).get('N', ''),
                'product_sale': item.get('product_sale', {}).get('BOOL', False),
                'product_category': item.get('product_category', {}).get('S', ''),
                'product_search_attributes': item.get('product_search_attributes', {}).get('S', ''),
                'product_reviews': item.get('product_reviews', {}).get('S', ''),
                'product_bom': item.get('product_bom', {}).get('S', ''),
                'product_assemblies': item.get('product_assemblies', {}).get('S', '')
            }
            return product_info
        else:
            print("Product not found.")
            return None
    except ClientError as e:
        print("Error getting product:", e)
        return None



#update product