#Jordan Divina - Tuesday, January 28, 2020
#Coding Challenge for RESTful Api with ElasticSearch

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from elasticsearch import Elasticsearch
import sys

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#Need to allow for local evaluator to change port
#Create ElasticSearch Object

def connectElasticSearch():

	UserValue = input()
	if UserValue == "":
		es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	else:
		es = Elasticsearch([{'host': 'localhost', 'port': UserValue}])

	#Checks to see if we properly connected to ElasticSearch
	if es.ping():
		print("Successfully connected")
	else:
		print("Oh no! Not connected!")
		sys.exit()
	return es;

#Need to create our index in ElasticSearch
def createIndex(es_object):
	#We are making an address book
	INDEX_NAME = "address"

	#Delete if it exists already in elasticSearch noSql database
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

		#This is for if there exists no query!
		#Very confused about the pageSize and page - I'll figure that out later if I have time
		if args['query'] == 'None' or args['query'] == None or args['query'] == 'none':
			allquery = {'size' : 10000,"query": {"match_all": {}}}
			res = es.search(index="address", body= allquery, scroll = '1m')
			res = res['hits']
			res = res['hits']
			empty_list = []
			for i in res:
				empty_list.append(i['_source'])
			num = args['pageSize']
			final = [empty_list[i * num:(i + 1) * num] for i in range((len(empty_list) + num - 1) // num )]
			return final

		#There exists some query if it did not go through the above if statement
		#Documentation seems very confusing for Python
		else:
			specialquery = args['query']
			print(specialquery)
			res = es.search(index = 'address', body=specialquery, scroll = '1m');
			if res == None or res == "None" or res == "none":
				return []
			res = res['hits']
			res = res['hits']
			empty_list = []
			for i in res:
				empty_list.append(i['_source'])
			num = args['pageSize']
			final = [empty_list[i * num:(i + 1) * num] for i in range((len(empty_list) + num - 1) // num )]
			return final

	#Creating the post for Contact endpoint
	#I'll return a print statement...

	def post(self):
		forumResults = request.get_json(force=True);

		Exists = es.exists(index = "address", id = forumResults["name"])
		if Exists:
			return "Name already exists in Address book; Did you maybe want to change it?"
		else:
			es.create(index = "address", id = forumResults["name"], body = forumResults);
			return "Success! Placed into address book"

#This class is specfically for endpoints /contact/name
#Most of this code follows the same pattern of checking if in address book
#If so, then perform action

class contactName(Resource):
	def get(self, name):
		Exists = es.exists(index = "address", id = name)
		if Exists:
			val =  es.get(index = "address", id = name)
			return val["_source"]
		else:
			return "Not in the address book!"

	#Had some trouble with the update elasticSeach Python, just changed to delete/create
	def put(self, name):
		forumResults = request.get_json(force=True);
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

api.add_resource(contact,'/contact')
api.add_resource(contactName, '/contact/<string:name>')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

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
	app.run(debug=True)











