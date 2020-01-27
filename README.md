# codingChallenge
A RESTful API for an address book with an Elasticsearch data store.

# Spec Definition

The form of the endpoint spec will be defined as:

VERB /path/{pathParam}/subpath?queryParam={}

The VERB is part of the HTTP spec and can be defined as GET, POST, PUT, DELETE (and a few others).  We will only be using the ones specified.

The path definition defines the URL path that we expect the api to be tied to.  

{pathParam} defines a variable element that should be interpreted by the API.  As an example:

Given the simple spec:

GET /user
GET /user/{name}

These endpoints would allow for the following URL paths:

/user
/user/bob
/user/jane
/user/sam

Additionally query parameters (?key=value) should be interpreted similarly but in the query string (everything after the ? in the URL).

Each endpoint should have a defined input and output, and should make sense to the person using it.

# API Definition

So for this API, the endpoints (aka methods) that we want in the api are as follows:

GET /contact?pageSize={}&page={}&query={}

This endpoint will providing a listing of all contacts, you will need to allow for a defined pageSize (number of results allowed back), and the ability to offset by page number to get multiple pages. Query also should be a query for queryStringQuery as defined by Elasticsearch that you can pass directly in the Elasticsearch call.

POST /contact

This endpoint should create the contact.  Given that name should be unique, this may need to be enforced manually.  

GET /contact/{name}

This endpoint should return the contact by a unique name. This name should be specified by the person entering the data.  

PUT /contact/{name}

This endpoint should update the contact by a unique name (and should error if not found)

DELETE /contact/{name}

This endpoint should delete the contact by a unique name (and should error if not found)
