from app import app
from flask import Flask, jsonify
from app import routes_reviews
#from app import dummydata_reviews

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8003, debug=True)

#dummydata_reviews.add_dummy_data()