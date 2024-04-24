#run using
#python -m unittest -v backend/orders/tests/test.py

import unittest



#check all apis work

#insert data

#get all data  --> check number of insertions is correct 

#create a new order --> save its id

#search for it using search api

#search using product id, status, user id, day

#change its status to shipped

#change its status to delivered

#retrieve it with the api using order id, check it matches expected output

#update item

#delete item

# check its not there anymore, gives appropriate error


#check quantity & price after adding to cart 

#check quantity & price after removing from 


#check errors

#wrong inputs / missing fields


class MultiplyTestCase(unittest.TestCase):

    def test_multiply_positive_numbers(self):

        result = 5

        self.assertEqual(result, 12)


