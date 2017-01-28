# Bucketlister
--
## Introduction
Bucketlister is a Flask API for a bucket list service. Its goal is to allow you to create bucketlist applications by exposing a simple API.

### URL Endpoints
--
The API specification is shown the following table:

| URL Endpoint | HTTP Methods | Summary | Requires Authentication |
| -------- | ------------- | --------- |-----------|
| `/api/auth/register` | `POST`  | Register a new user| False |
| `/api/auth/login/` | `POST` | Logins user and generates authentication token| False |
| `/api/bucketlists/` | `POST` | Create a new Bucketlist | True |
| `/api/bucketlists/` | `GET` | Fetches all the created bucket lists | True |
| `/api/bucketlists/?limit=<limit>` | `GET` | Fetches all bucketlists, paginated by `limit` bucketlists per page where `limit` is an integer with a maximum value of 100| True |
| `/api/bucketlists/?q=<bucketlist_name>` | `GET` | Fetches all bucketlists whose name contain the string `bucketlist_name` | True |
| `/api/bucketlists/<id>` | `GET` | Fetches a single bucket list, with id `id` | True |
| `/api/bucketlists/<id>` | `PUT` | Updates a single bucket list with id `id` | True |
| `/api/bucketlists/<id>/` | `DELETE` | Delete a bucket list with id `id`| True |
| `/api/bucketlists/<id>/items/` | `POST` |  Create a new item in a bucket list | True |
| `/api/bucketlists/<id>/items/<item_id>/` | `DELETE`| Delete an item in a bucket list| True |
| `/api/bucketlists/<id>/items/<item_id>/` | `PUT`| Updates an item in a bucketlist| True |

### Setup
-
Bucketlister is developed and tested on Python 3. The recommended versions are Python 3.5 and 3.6.

Follow the following steps to have the system up and running:

* Prepare a virtual environment using virtualenv or virtualenvwrapper

* Clone this repository with:
  * HTTPS:
  
  		`git clone https://github.com/andela-mkamau/bucketlist_api.git`
  		
  * SSH:

  		`git clone git@github.com:andela-mkamau/bucketlist_api.git`

* Prepare a virtual environment to install the application. Within the virtual environment, install the application dependancies with:

	   `pip install -r requirements.txt`
	
* Start the application server with:

	`python manage.py runserver`

At this point, Bucketlister will be ready to receive HTTP requests.

### Usage
-
The examples below use curl to make requests.

**Create User Account**

Make a POST request the endpoint `/api/auth/register` with a username and password combination in the body of the request. 

```
curl -i -H "Content-Type: application/json" -d '{"username": "jane", "password":"1..m"}' -X POST http://127.0.0.1:5000/api/auth/register
```

Upon creating a new user, the server responds with a response with:

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Thu, 26 Jan 2017 20:16:19 GMT
{
  "id": 82,
  "username": "jane"
}
```

**Log in User**

To log in a User, make a POST request to the endpoint `/api/auth/login/`. 




	
		
		




