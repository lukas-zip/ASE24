# importing modules 
from reportlab.pdfgen import canvas 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
import boto3
from app import dynamodb_users, dynamodb_po, utils, initialise_dynamo
import json
from botocore.exceptions import ClientError
from io import BytesIO
import requests

s3_invoice = initialise_dynamo.s3_client

# Create S3 bucket on LocalStack
def create_s3_bucket():
    try:
        bucket_name = "invoice-bucket"
        s3_invoice.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")
def get_invoice(order_id):
    try:
        object_key = f'invoice_{order_id}.pdf'
        # List Objects in Buckets
        response_list = s3_invoice.list_objects(Bucket='invoice-bucket')
        response_obj = s3_invoice.get_object(Bucket='invoice-bucket', Key=object_key)
        # Iterate over the objects in the response
        if 'Contents' in response_list:
            for obj in response_list['Contents']:
                if obj['Key'] == object_key:
                    # Return Object Name
                    return obj['Key'], True
                    # Return Object
                    #object_data = response_obj['Body'].read()
                    #return object_data, True
        else:
            return "Not successful (get function)", False
    except ClientError as e:
        print("Error creating invoice:", e)
        return "Error creating invoice!", e

# create the invoice pdf for an orde and store it in s3 bucket
def create_pdf(order_id):
    try:
        buffer = BytesIO()

        # get the order information new
        response_order = requests.get(f'http://orders:8004/orders/{order_id}')
        order_details = response_order.json()
        total_price = order_details['total_price']
        product_list = order_details['orders_fe'] #list with order lines (id, owner and quantity)
        user_id = order_details['user_id'] #just name, adress missing
        response_user = requests.get(f'http://user-service:8001/users/{user_id}')
        user_details = response_user.json()
        shipping_adress = user_details['value']['address']
        user_name = user_details['value']['username']

        # creating a pdf object 
        fileName = f'invoice_{order_id}.pdf'
        pdf = canvas.Canvas(fileName, pagesize=letter)
        # Define layout parameters
        top_margin = 730
        table_start = 480
        page_width, page_height = letter
        # Draw order ID and "Invoice"
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, top_margin, f'Order ID: {order_id}')
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawRightString(page_width - 50, top_margin, 'Invoice')
        # Draw separation line
        pdf.setFont("Helvetica", 12)
        pdf.line(50, top_margin - 20, page_width - 50, top_margin - 20)
        # Draw shipping and billing addresses
        pdf.drawString(50, top_margin - 50, f'Shipping Address: ')
        pdf.drawString(50, top_margin - 65, f'{user_name}')
        pdf.drawString(50, top_margin - 80, f'{shipping_adress}')
        pdf.drawString(300, top_margin - 50, f'Bill To: ')
        pdf.drawString(300, top_margin - 65, f'{user_name}')
        pdf.drawString(300, top_margin - 80, f'{shipping_adress}')
        pdf.drawString(50, top_margin - 195, f'Thank you for your order.')

        # Create table for products new
        data = [["Product Name", "Quantity", "Price", "Discount", "Reduced Price"]]
        for no in range(len(product_list)): #hier noch pro product
            product_id = product_list[no]['product_id']
            product_quantity = product_list[no]['quantity']
            product_price, product_disc, product_owner = utils.get_product_details(product_id)
            reduced_price = utils.calc_discounted_price(product_price, product_disc)
            response_product = requests.get(f'http://inventory_management:8002/product/{product_id}')
            product_details = response_product.json()
            product_name = product_details['value']['product_name']
            data.append([product_name, product_quantity ,product_price, product_disc, reduced_price ])
        table_width = page_width - 100  # Adjusted width for table
        table = Table(data, colWidths=[table_width / 5] * 5)  # Equal width for each column
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        table.wrapOn(pdf, 0, 0)
        table.drawOn(pdf, 50, table_start)
        # Add total price
        pdf.drawRightString(page_width - 50, table_start - 30, f'Total Price: {total_price}')
        pdf.drawString(50, 110, f'Other comments:')
        pdf.drawString(50, 90, f'- Already payed with credit card')
        pdf.drawString(50, 70, f'- Our general terms and conditions apply')
        ##add shop details
        #pdf.drawRightString(page_width - 50, 50 , f'//Store details')

        # saving the pdf 
        pdf.save()

        # store pdf in s3 bucket
        object_key = f'invoice_{order_id}.pdf'
        upload_pdf(buffer, "invoice-bucket", object_key)
        
        item, status = get_invoice(order_id)
        if status == True:
            return "Successfully uploaded (create function)", True
        else: 
            return "Not successful (create function)", False
    
    except ClientError as e:
        print("Error getting review:", e)
        return "Error getting review!", e
    
def upload_pdf(file, bucket_name, object_key):
    try:
        s3_invoice.put_object(Body=file.getvalue(), Bucket=bucket_name, Key=object_key)
        return True
    except ClientError as e:
        print("Error uploading file to S3:", e)