#Jordan Divina - Tuesday, January 28 2020
#code for testing purposes

import requests
import unittest

#Make sure to run these tests with a completely empty elasticSearch
#These tests are to ensure proper storage and retreival aspects of code
#In the code, I made the document ID the name because that has to be unique I believe

URL = "http://localhost:5000/contact"
sampleQuery = '{"name": "Jackson","number": 1234567890,"address": "notHere","birthday": "12/12/2020"}'

testURL = "http://127.0.0.1:5000/contact/Jackson"

#I guess it might be a bit circular
#But I'll first add to the database
#Then I'll check if we get the correct response down below
x = requests.post(url = URL, data = sampleQuery)

class contactWithName(unittest.TestCase):

	#Tests if it exists
	def test_get(self):
		x = requests.get(testURL);
		data = x.json()
		self.assertEqual(data, {"name": "Jackson", "number": 1234567890, "address": "notHere", "birthday": "12/12/2020"})

	#Test if it doesn't exists
	def test_getNotExists(self):
		randomURL = "http://127.0.0.1:5000/contact/Jordan"
		x = requests.get(randomURL)
		data = x.json()
		self.assertEqual(data, "Not in the address book!")

	#Test if put works
	def test_put(self):
		changeVal = '{"name": "Jackson","number": 1234567890,"address": "Charlottesville, VA","birthday": "10/12/1980"}'
		requests.put(testURL, changeVal);
		y = requests.get(testURL);
		eata = y.json()
		self.assertEqual(eata, {"name": "Jackson", "number": 1234567890, "address": "Charlottesville, VA", "birthday": "10/12/1980"})

	#Test if put works on non existent item
	def test_putNotExists(self):
		requests.put(testURL, sampleQuery);
		randomURL = "http://127.0.0.1:5000/contact/Jordan"
		x = requests.put(randomURL, sampleQuery);
		data = x.json()
		self.assertEqual(data, "Not in the address book!")

	#Test if we try to place a wrong item
	def test_WrongNumber(self):
		changeVal = '{"name": "Jackson","number": 12890,"address": "Charlottesville, VA","birthday": "10/12/1980"}'
		x = requests.put(testURL, changeVal);
		eata = x.json()
		self.assertEqual(eata, "Not a valid number, please try again")

	#Test deleting
	def test_delete(self):
		requests.delete(testURL);
		x = requests.get(testURL);
		requests.post(url = URL, data = sampleQuery)
		data = x.json()
		self.assertEqual(data, "Not in the address book!")

	#Testing if item exists, if not, then do nothing
	def test_deleteNotExists(self):
		randomURL = "http://127.0.0.1:5000/contact/Jordan"
		x = requests.delete(randomURL)
		data = x.json()
		self.assertEqual(data, "Not in the address book!")

	#Below we are testing contact
	#Try to post to same name
	def test_postSame(self):
		requests.post(URL, sampleQuery)
		x = requests.post(URL, sampleQuery)
		data = x.json()
		self.assertEqual(data, "Name already exists in Address book. Did you maybe want to change it?")

	#Repeating the code from above
	def test_postNew(self):
		coolQuery = '{"name": "Jason","number": 1234567890,"address": "Here","birthday": "11/11/2010"}'
		requests.post(URL, coolQuery);
		x = requests.get(URL+"/Jason")
		data = x.json()
		self.assertEqual(data, {"name": "Jason", "number": 1234567890, "address": "Here", "birthday": "11/11/2010"})

if __name__ == '__main__':
    unittest.main()




