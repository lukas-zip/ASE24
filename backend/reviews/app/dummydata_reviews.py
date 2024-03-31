from app import dynamodb_reviews

# Function to add dummy users
def add_dummy_data():
    dummy_review = [
        {"product_id": "1234", "customer_id": "4321", "reviewcontent": "Greate Design", "rating": "5", "time_lastedit": "20.03.2024 - 11:50:00", "time_created": "20.03.2024 - 11:50:00"},
    ]
    # Adding dummy users
    for review in dummy_review:
        dynamodb_reviews.add_review(product_id=review["product_id"], customer_id=review["customer_id"], reviewcontent=review["reviewcontent"], rating=review["rating"], time_lastedit=review["time_lastedit"], time_created=review["time_created"])
