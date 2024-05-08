from flask import request, jsonify, Blueprint
from app import dynamodb_po, dynamodb_users, invoice
from botocore.exceptions import ClientError
from app import utils

route_blueprint = Blueprint('', __name__,)

# Test if endpoint is available
@route_blueprint.route('/', methods=['GET'])
def test():
   # Return success response
   return jsonify({'status': True, 'message': 'Test successful'}), 201


@route_blueprint.route("/orders/<order_id>", methods=['GET'])
def get_order_req(order_id):
   try:
       # Check if the order_id parameter is provided
       if not order_id:
           return jsonify({'error': 'Order ID is missing', 'status': False}), 400
      
       # Call the get_order function
       res = dynamodb_users.get_order(order_id)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500


@route_blueprint.route("/orders", methods=['GET'])
def get_all_orders_req():
   try:
       # Call the get_all_orders function
       res = dynamodb_users.get_all_orders()
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500




@route_blueprint.route("/orders/<order_id>", methods=['DELETE'])
def delete_order_req(order_id: int):   
   try:
       # Check if the order_id parameter is provided
       if not order_id:
           return jsonify({'error': 'Order ID is missing', 'status': False}), 400
      
       # Call the delete_order function
       res = dynamodb_users.delete_order(order_id)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500




@route_blueprint.route("/orders/<order_id>", methods=['PUT'])
def update_order_req(order_id):
   data = request.json
   # Check if all required parameters are present
   required_params = ['product_id', 'quantity']
   if not all(param in data for param in required_params):
       return jsonify({'status': False,'value': 'Missing required parameters'}), 400

   try:
        res = dynamodb_users.update_order(order_id, data['product_id'], data['quantity'])
        return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       print(e)
       return jsonify({'status': False, 'value': str(e)}), 500



@route_blueprint.route("/orders/users/search/<user_id>", methods=['GET'])  
def search_orders(user_id):
   data = request.json
   try:
       # Check if all required parameters are present
       if not user_id:
           return jsonify({'error': 'User ID is missing', 'status': False}), 400
      
       # Call search_orders function
       res = dynamodb_users.search_orders(user_id)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500




@route_blueprint.route("/orders", methods=['POST'])   
def add_order_req():
   data = request.json


   # Check if all required parameters are present
   required_params = ['user_id', 'product_id', 'quantity']
   if not all(param in data for param in required_params):
       return jsonify({'status': False, 'value': 'Missing required parameters'}), 400
  
   if data['quantity'] <= 0:
       return jsonify({'status': False,'message': 'order quantity should be at least 1'}), 400
  
   # If all checks pass, proceed to add the order
   try:
       res = dynamodb_users.add_item(data['user_id'],data['product_id'], data['quantity'])
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       return jsonify({'status': False,'value': str(e)}), 500




@route_blueprint.route("/orders/product/search/<product_owner_id>", methods=['GET']) 
def search_po_orders(product_owner_id):
   try:
       # Check if the product_owner_id parameter is provided
       if not product_owner_id:
           return jsonify({'error': 'Product owner ID is missing', 'status': False}), 400
      
       # Call the search_orders_by_po function
       res = dynamodb_po.search_orders_by_po(product_owner_id)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500


@route_blueprint.route("/orders/product/search/status/<order_status>", methods=['GET'])  
def search_po_orders_status(order_status):
   try:
       # Check if the order_status parameter is provided
       if not order_status:
           return jsonify({'error': 'Order Status is missing', 'status': False}), 400


       if order_status not in ['paid', 'unpaid']:
           return jsonify({'error': 'Order Status has to be one of paid, unpaid', 'status': False}), 400
       # Call the search_orders_by_status function
       res = dynamodb_po.search_po_orders_by_status(order_status)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500


@route_blueprint.route("/orders/search/user/<user_id>/status/<order_status>", methods=['GET'])
def search_orders_status_and_user_id(user_id,order_status):
   try:
       # Check if both user_id and order_status parameters are provided
       if not user_id or not order_status:
           return jsonify({'error': 'User ID or Order status is missing', 'status': False}), 400


       if order_status not in ['paid', 'unpaid']:
           return jsonify({'error': 'Order Status has to be one of paid, unpaid', 'status': False}), 400
      
       # Call the search_orders_by_status function
       res = dynamodb_users.search_orders_by_userid_and_status(user_id, order_status)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500


# @route_blueprint.route("/orders/search/po/<user_id>/status/<order_status>", methods=['GET'])
# def search_po_orders_status_and_user_id(user_id,order_status):
#    try:
#        # Check if both user_id and order_status parameters are provided
#        if not user_id or not order_status:
#            return jsonify({'error': 'User ID or Order status is missing', 'status': False}), 400


#        if order_status not in ['paid', 'unpaid']:
#            return jsonify({'error': 'Order Status has to be one of paid, unpaid', 'status': False}), 400
      
#        # Call the search_orders_by_status function
#        res = dynamodb_po.search_orders_by_userid_and_status(user_id, order_status)
      
#        # Return the response
#        return jsonify({'status': True, 'value': res}), 200
#    except Exception as e:
#        # If an exception occurs, return an error response
#        return jsonify({'error': str(e), 'status': False}), 500


@route_blueprint.route("/orders/search/po/<po_id>/status/<order_status>", methods=['GET'])
def search_orders_status_and_po_id(po_id,order_status):
   try:
       # Check if both user_id and order_status parameters are provided
       if not po_id or not order_status:
           return jsonify({'error': 'PO ID or Order status is missing', 'status': False}), 400


       if order_status not in ['paid', 'unpaid']:
           return jsonify({'error': 'Order Status has to be one of paid, unpaid', 'status': False}), 400
      
       # Call the search_orders_by_status function
       res = dynamodb_po.search_orders_by_po_id_and_status(po_id, order_status)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500




@route_blueprint.route("/orders/product/<order_id>/<product_owner_id>/paid", methods=['GET']) 
def set_po_orders_paid(order_id, product_owner_id):
   try:
       # Check if both order_id and product_owner_id parameters are provided
       if not order_id or not product_owner_id:
           return jsonify({'error': 'Order ID or Product owner ID is missing', 'status': False}), 400
      
       # Call the update_po_status function
       res = dynamodb_po.update_po_status(product_owner_id, order_id, 'paid')
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500


from flask import jsonify, abort

@route_blueprint.route("/orders/<order_id>/status/paid", methods=['GET'])
def set_user_order_status_paid(order_id):
    try:
        res = dynamodb_users.update_status(order_id, 'paid')
        return jsonify({'status': True, 'value': res}), 200
    except Exception as e:
        # Return an appropriate error response
        return jsonify({'status': False, 'error': 'Internal Server Error'}), 500

@route_blueprint.route("/orders/search/status/<status>", methods=['GET'])  
def search_user_order_by_status(status):
    try:
        res = dynamodb_users.search_orders_by_status(status)
        return jsonify({'status': True, 'value': res}), 200
    except ValueError as ve:
        # Handle specific error if needed
        return jsonify({'status': False, 'error': str(ve)}), 400
    except Exception as e:
        # Return an appropriate error response
        return jsonify({'status': False, 'error': 'Internal Server Error'}), 500



# ----------------------------------------------------------------------------#
# Invoice APIs
# ----------------------------------------------------------------------------#
# Create a invoice pdf out of the order details for one order
@route_blueprint.route("/invoice/<order_id>'", methods=['POST']) 
def route_create_invoice(order_id):
   if not order_id:
       return jsonify({'error': 'ID is required!'}), 400
   try:
       message, status = invoice.create_pdf(order_id)
       if status == True:
           return jsonify({'value': message,'status': status}), 200
       else:
           return jsonify({'message': message,'status': status}), 200
   except ClientError as e:
       print("Error adding review:", e)


## Download the invoice for a specific order
@route_blueprint.route("/invoice/<order_id>'", methods=['GET'])
def route_get_invoice(order_id):
   if not order_id:
       return jsonify({'error': 'ID is required!'}), 400
   try:
       item, status = invoice.get_invoice(order_id)
       return jsonify({'value': item,'status': status}), 200    
   except ClientError as e:
       print("Error adding review:", e)
       return jsonify({'error': 'Failed to get review'}), 500




# ----------------------------------------------------------------------------#
# Testing APIs
# ----------------------------------------------------------------------------#


@route_blueprint.route("/orders/test/<product_id>", methods=['GET'])
def test_orders(product_id):
   try:
       # Check if the product_id parameter is provided
       if not product_id:
           return jsonify({'error': 'Product ID is missing', 'status': False}), 400
      
       # Call the get_product_details function
       res = utils.get_product_details(product_id)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500


@route_blueprint.route("/orders/po", methods=['GET'])  
def get_all_po_orders():
   try:
       # Call the get_all_po_orders function
       res = dynamodb_po.get_all_po_orders()
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500




@route_blueprint.route("/orders/po/test/search/order_id/<order_id>", methods=['GET'])    
def search_po_orders_orderid(order_id):
   try:
       # Check if the order_id parameter is provided
       if not order_id:
           return jsonify({'error': 'Order ID is missing', 'status': False}), 400
      
       # Call the search_orders_by_orderid function
       res = dynamodb_po.search_orders_by_orderid(order_id)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500


@route_blueprint.route("/orders/test/po/search/<order_id>/<product_owner_id>", methods=['GET']) 
def test_search_po_orders(order_id,product_owner_id):
   try:
       # Check if both order_id and product_owner_id parameters are provided
       if not order_id or not product_owner_id:
           return jsonify({'error': 'Order ID or Product owner ID is missing', 'status': False}), 400
      
       # Call the search_po_orders function
       res = dynamodb_po.search_po_orders(product_owner=product_owner_id, order_id=order_id)
      
       # Return the response
       return jsonify({'status': True, 'value': res}), 200
   except Exception as e:
       # If an exception occurs, return an error response
       return jsonify({'error': str(e), 'status': False}), 500




# ----------------------------------------------------------------------------#
# Error Handling.
# ----------------------------------------------------------------------------#


@route_blueprint.app_errorhandler(400)
def unprocessable(error):
   return jsonify({
       'success': False,
       'value': 'bad request'
   }), 400




@route_blueprint.app_errorhandler(404)
def not_found(error):
   return jsonify({
       'success': False,
       'value': 'resource not found'
   }), 404




@route_blueprint.app_errorhandler(405)
def method_not_allowed(error):
   return jsonify({
       'success': False,
       'value': 'method not allowed'
   }, 405)




@route_blueprint.app_errorhandler(422)
def unprocessable(error):
   return jsonify({
       'success': False,
       'value': 'unprocessable'
   }), 422




@route_blueprint.app_errorhandler(500)
def internal_server_error(error):
   return jsonify({
       'success': False,
       'value': 'Internal Server Error'
   }, 500)

