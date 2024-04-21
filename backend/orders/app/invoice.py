# importing modules 
from reportlab.pdfgen import canvas 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
import boto3
from app import dynamodb
import json
from botocore.exceptions import ClientError
from io import BytesIO

s3_invoice = dynamodb.s3_client

# Create S3 bucket on LocalStack
def create_s3_bucket():
    try:
        bucket_name = "invoice-bucket"
        s3_invoice.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} created successfully.")
    except ClientError as e:
        print(f"Error creating bucket: {e}")


# create the invoice pdf for an orde and store it in s3 bucket
def create_pdf(order_id):
    try:
        # generate pdf 
        pdf = generate_pdf(order_id)
        object_key = f'invoice_{order_id}.pdf'

        # store pdf in s3 bucket
        upload_pdf(pdf, "invoice-bucket", object_key)

        return "sucessfully created pdf", True
    except ClientError as e:
        print("Error getting review:", e)
        return "Error getting review!", e

# generate the invoice 
def generate_pdf(order_id):

    buffer = BytesIO()

    # get the order information
    order_details = dynamodb.get_order(order_id)
    strorder = json.dumps(order_details)

    # dummy order info - delte later
    order_info = {
        "order_id":  order_id,
        "orders":  [
            {"product_id": "product_id1", "product_name": "Product 1", "price": 100},
            {"product_id": "product_id2", "product_name": "Product 2", "price": 150},
            {"product_id": "product_id3", "product_name": "Product 3", "price": 40}
        ],
        "total_price":  290
    }

    # creating a pdf object 
    fileName = f'invoice_{order_id}.pdf'
    pdf = canvas.Canvas(fileName, pagesize=letter)

    # Define layout parameters
    top_margin = 730
    table_start = 480
    page_width, page_height = letter

    # Draw order ID and "Invoice"
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, top_margin, f'Order ID: {order_info["order_id"]}')
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawRightString(page_width - 50, top_margin, 'Invoice')

    # Draw separation line
    pdf.setFont("Helvetica", 12)
    pdf.line(50, top_margin - 20, page_width - 50, top_margin - 20)

    # Draw shipping and billing addresses
    pdf.drawString(50, top_margin - 50, f'Shipping Address: //Shipping Address')
    pdf.drawString(300, top_margin - 50, f'Bill To: //Billing Address')

    pdf.drawString(50, table_start + 15, f'Thank you for your order.')

    # Create table for products
    data = [["Product ID", "Product Name", "Price"]]
    for order in order_info["orders"]:
        data.append([order["product_id"], order["product_name"], str(order["price"])])
    
    table_width = page_width - 100  # Adjusted width for table
    table = Table(data, colWidths=[table_width / 3] * 3)  # Equal width for each column
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
    pdf.drawRightString(page_width - 50, table_start - 30, f'Total Price: ${order_info["total_price"]}')
    pdf.drawString(50, 150, f'Orderdate: //Date')
    pdf.drawString(50, 110, f'Other comments:')
    pdf.drawString(50, 90, f'- Already payed with credit card')
    pdf.drawString(50, 70, f'- Our general terms and conditions apply')

    pdf.drawRightString(page_width - 50, 50 , f'//Store details')

    # saving the pdf 
    pdf.save()

    #return buffer
    return buffer
    
def upload_pdf(file, bucket_name, object_key):
    try:
        s3_invoice.put_object(Body=file.getvalue(), Bucket=bucket_name, Key=object_key)
        return True
    except ClientError as e:
        print("Error uploading file to S3:", e)
