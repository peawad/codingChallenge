# codingChallenge by Jordan Divina [Documentation and Thoughts]

A RESTful API for an address book with an elasticsearch data store. The specifications can be shown in the shared googleDoc provided by company

## Please read here:
- - - - - - - - - - - - - - - - - - - - - - - - - 

I'll be using Flask/Flask_restful to create this RESTful API
I'll also use the ElasticSearch as directed in the instructions

- **Python: 3.6.8**
- **elasticSearch: 7.5.2**
- **Flask: 1.1.1**
- Using latest version of **Flask Restful**
- Using latest version of **Python elasticSearch** for 7.5.2
- Also using **request** for testing purposes in test.py

## Setting up the environment

Please download or clone the repository above. Before we begin, you will have to configure your elasticSearch server. Afterwards, run main.py as such (python3 main.py or python main.py) in terminal.

You will then be prompted with an input. Place your specific port number. If it successfully connects, then you are good! However, if it fails (or you misstyped), you will be exited out the program. By default, if you just press enter, then it will default to the normal 9200 port for elasticSearch. However, I do not allow for the flask port to be changed!

Now, you can run all get, post, put, and delete in your browser!

Also, if you want to run test.py, then run it the same as main.py. However, make sure that you run it when the elasticSearch database is empty

## Creating the data model

For purposes of the challenge, I was tasked in creating a data model for an address book. Therefore, in order to keep it simple, a **contact** consists of only a name, a number, an address, and a birthday. It would be best to keep things simple for someone's first attempt in creating a RESTFUL API. Please note, that birthday is kept as a string. This is not best practice, and I hope to change this for later iterations.
