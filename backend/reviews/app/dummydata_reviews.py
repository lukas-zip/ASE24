from app import dynamodb_reviews

# Function to add dummy users
def add_dummy_data():
    dummy_review = [
        {"product_id": "1234", "customer_id": "4321", "reviewcontent": "Greate Design", "rating": "5"},
    ]
    # Adding dummy users
    for review in dummy_review:
        dynamodb_reviews.add_review(product_id=review["product_id"], customer_id=review["customer_id"], reviewcontent=review["reviewcontent"], rating=review["rating"])
