#Jordan Divina - Tuesday, January 28, 2020
#Coding Challenge for RESTful Api with ElasticSearch


#Using flask_restful might be a bit cheating
#However, I think it really improves readability vs just vanilla flask
#I would also like to state that I am running Python 3.6.8

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from elasticsearch import Elasticsearch
import sys

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Very elementary way to count number of digits in number
#Only counts number of digits; if I had more time, then I would of have made
#this function more elegant; I would also check for format like
# ***-***-**** or (***) *** **** using add on re

def isValid(s):
	
	if s < 0:
		return False

	digits = len(str(s))
	if digits == 10 or digits == 11:
		return True
	else:
		return False	

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Need to allow for evaluator to change port for local
#However, the flask local port will be the default - sorry!
#Create ElasticSearch Object

def connectElasticSearch():

	UserValue = input()
	if UserValue == "":
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	else:
		es = Elasticsearch([{'host': 'localhost', 'port': UserValue}])

	#Checks to see if we properly connected to ElasticSearch
	if es.ping():
		print("++++++++++++++++++++++")
		print("Successfully connected")
		print("++++++++++++++++++++++")
		print("")
	else:
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Oh no! Not connected!")
		print("Exiting...")
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		sys.exit()
	return es;

#Need to create our index in ElasticSearch
def createIndex(es_object):
	#We are making an address book
	INDEX_NAME = "address"

	#Delete if it exists already in elasticSearch noSql database
	#Just for easy reset of index and testing
	es_object.indices.delete(index = INDEX_NAME, ignore = 404)
	es_object.indices.create(
		index = INDEX_NAME,
		body = {
			'mappings':{},
			'settings':{}
		},
	)
	return es_object;

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Need to create the Flask app, and also the api by documentation standards

app = Flask(__name__)
api = Api(app)

#Creating classes to handle all the VERB requests
#Generic contact class to handles endpoints of the form /contact

class contact(Resource):

	#Creating the Get for Contact
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('pageSize', type = int)
		parser.add_argument('page', type = int)
		parser.add_argument('query', type = str)
		args = parser.parse_args()

		#More edge cases
		#Wil throw error message if pageSize or page were none
		#This is just to make sure
		if args['pageSize'] <= 0:
			args['pageSize'] = 10;

		if args['page'] <= 0:
			args['page'] = 5;	

		#This is for if there exists no query!
		#Very confused about the pageSize and page - I'll figure that out later if I have time
		#and I'll ask the person grading what it means or what they expected

		if args['query'] == 'None' or args['query'] == None or args['query'] == 'none':
			allquery = {'size' : 10000,"query": {"match_all": {}}}
			res = es.search(index="address", body= allquery, scroll = '1m') #Nice trick I found online!
			res = res['hits']
			res = res['hits']
			empty_list = []
			for i in res:
				empty_list.append(i['_source'])

			#Below is my guess on the pagination - make list of lists
			#Then choose from the number of lists wanted
			#so I can properly put on pages on web
			#however, not entirely sure

			num = args['pageSize']
			final = [empty_list[i * num:(i + 1) * num] for i in range((len(empty_list) + num - 1) // num )]
			return final

		#There exists some query if it did not go through the above if statement
		#elasticSearch Documentation seems very confusing for Python
		#Not many good examples online

		#Also I have tested this code for query_strings!

		else:
			specialquery = args['query']
			res = es.search(index = 'address', body=specialquery, scroll = '1m')
			if res == None or res == "None" or res == "none":
				return []
			res = res['hits']
			res = res['hits']
			empty_list = []
			for i in res:
				empty_list.append(i['_source'])

			#same code from above
			num = args['pageSize']
			final = [empty_list[i * num:(i + 1) * num] for i in range((len(empty_list) + num - 1) // num )]
			return final

	#Creating the post for Contact endpoint
	#I'll return a string...

	def post(self):
		forumResults = request.get_json(force=True);

		valid = isValid(forumResults["number"])
		if valid == False:
			return "Not a valid number, please try again"

		Exists = es.exists(index = "address", id = forumResults["name"])
		if Exists:
			return "Name already exists in Address book. Did you maybe want to change it?"
		else:
			es.create(index = "address", id = forumResults["name"], body = forumResults);
			return "Success! Placed into address book"

#This class is specfically for endpoints /contact/name
#Most of this code follows the same pattern of checking if in address book
#If so, then perform action
#If not, then just skip and return message

class contactName(Resource):
	def get(self, name):
		Exists = es.exists(index = "address", id = name)
		if Exists:
			val =  es.get(index = "address", id = name)
			return val["_source"]
		else:
			return "Not in the address book!"

	#Had some trouble with the update elasticSeach Python, just changed to delete/create
	#I do imagine that it is a bit slower
	#I'll figure out the small details later

	def put(self, name):
		forumResults = request.get_json(force=True);

		#Checks if updated number is legit
		valid = isValid(forumResults["number"])
		if valid == False:
			return "Not a valid number, please try again"

		Exists = es.exists(index = "address", id = name)
		if Exists:
			es.delete(index="address", id = name)
			es.create(index = "address", id = name, body = forumResults);
			return "Updated!"
		else:
			return "Not in the address book!"

	def delete(self, name):
		Exists = es.exists(index = "address", id = name)
		if Exists:
			es.delete(index="address", id = name)
			return "Deleted"
		else:
			return "Not in the address book!"

#This is how we define the endpoints!
api.add_resource(contact,'/contact')
api.add_resource(contactName, '/contact/<string:name>')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#Time to run main method!

if __name__ == '__main__':

	#Message for user
	print("====================================================")
	print("Please provide the port number for the elasticsearch")
	print("By default, the localhost will be configured to 9200")
	print("====================================================")

	#Creating the ElasticSearch Object
	#Also deleting index AddressBook if it already exists
	es = connectElasticSearch();
	es = createIndex(es);

	#Then run the App!
	app.run(debug=False)
	
