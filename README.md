[![Build Status](https://travis-ci.org/andela-mkamau/bucketlist_api.svg?branch=develop)](https://travis-ci.org/andela-mkamau/bucketlist_api)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7303f0f8dc2a4f7dbdabff2f2dd8f040)](https://www.codacy.com/app/michael-kamau/bucketlist_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-mkamau/bucketlist_api&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/7303f0f8dc2a4f7dbdabff2f2dd8f040)](https://www.codacy.com/app/michael-kamau/bucketlist_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-mkamau/bucketlist_api&amp;utm_campaign=Badge_Coverage)
# Bucketlister

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

Make a POST request to the endpoint `/api/auth/register` with a username and password combination in the body of the request. 

```
curl -i -H "Content-Type: application/json" -d '{"username": "jane", "password":"1..m"}' -X POST http://127.0.0.1:5000/api/auth/register
```

Upon creating a new user, the server responds with the response:

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 88
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 19:06:30 GMT

{
  "id": 2, 
  "message": "Jane account created successfully", 
  "username": "jane"
}

```

**Log in User**

To log in a User, make a POST request to the endpoint `/api/auth/login/` with correct username and password. For instance:

```
curl -i -H "Content-Type: application/json" -d '{"username": "jane", "password":"1..m"}' -X POST http://127.0.0.1:5000/api/auth/login 
```

After successful authentication, the server responds with an access token to be used for future authentication. 
NOTE: This token valid for only an hour, after which one is required to log in again to obtain another one.

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 176
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 19:07:50 GMT

{
  "message": "user authenticated", 
  "token": "eyJpYXQiOjE0ODU3MTY4NzAsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIwNDcwfQ.eyJpZCI6Mn0.9REbFnvsHDQYFapQmOnj4fItg1t4FhC1lf1mFAs0KzA"
}

```

**Create a Buckelist**

To create a new bucketlist, make a POST request to the endpoint `/api/bucketlists/`. The body of the request must include the `name` and [optional] `description` of the bucketlist. 

Note that you must include the correct authentication token within the `Authorization` header of the request. For instance:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MTY4NzAsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIwNDcwfQ.eyJpZCI6Mn0.9REbFnvsHDQYFapQmOnj4fItg1t4FhC1lf1mFAs0KzA" -d '{"name": "Travel Kenya", "description":"A great plan to travel and see my country"}' -X POST http://127.0.0.1:5000/api/bucketlists/ 
```

Upon successfully creating the bucketlist, the server responds with:

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Location: http://127.0.0.1:5000/api/bucketlists/1
Content-Length: 113
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 19:31:45 GMT

{
  "message": "created bucketlist successfully", 
  "resource url": "http://127.0.0.1:5000/api/bucketlists/1"
}

```

**Editing a Bucketlist**

One can edit a bucketlist `name` and `description`. To do so, make a PUT request to the endpoint `/api/bucketlists/<id>` replacing `<id>` with the correct bucketlist id. For instance:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MTk5OTcsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIzNTk3fQ.eyJpZCI6NX0.JVNifJJqUZYkTVAW6cJD6aExXdkEMyO7r4NWlAJBm44" -d '{"name": "Climb the tallest mountain in Kenya", "description":"This will be great"}' -X PUT http://127.0.0.1:5000/api/bucketlists/2

```

On successfully editing the bucketlist, the server responds with:

```
{
  "message": "successfully updated bucketlist", 
  "resource url": "http://127.0.0.1:5000/api/bucketlists/2"
}

```

**Deleting a Bucketlist**

To delete a bucketlist, make a DELETE request to the endpoint `/api/bucketlists/<id>/`, replacing `<id>` with the correct bucketlist `id`. For instance to delete the bucketlidt with `id` 2:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MTk5OTcsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIzNTk3fQ.eyJpZCI6NX0.JVNifJJqUZYkTVAW6cJD6aExXdkEMyO7r4NWlAJBm44"  -X DELETE  http://127.0.0.1:5000/api/bucketlists/2 

```

After deletion, the server responds with status code 204 to indicate that the bucketlist has been removed:

```
HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 0
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 20:21:21 GMT

```

**Retrieve all bucketlists**

To retrieve all bucketlists, make a GET request to the endpoint `/api/bucketlists/`. For instance:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MTk5OTcsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIzNTk3fQ.eyJpZCI6NX0.JVNifJJqUZYkTVAW6cJD6aExXdkEMyO7r4NWlAJBm44" -X GET http://127.0.0.1:5000/api/bucketlists/    

```

The server responds with a list of bucketlists:

```
[
  {
    "created_by": 5, 
    "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
    "date_modified": null, 
    "description": "", 
    "id": 3, 
    "items": [], 
    "name": "Build a House"
  }, 
  {
    "created_by": 5, 
    "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
    "date_modified": null, 
    "description": "", 
    "id": 4, 
    "items": [], 
    "name": "Plant 1000 tree seedlings"
  }, 
  {
    "created_by": 5, 
    "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
    "date_modified": null, 
    "description": "", 
    "id": 13, 
    "items": [], 
    "name": "Learn to cook"
  }, 
  {
    "created_by": 5, 
    "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
    "date_modified": null, 
    "description": "", 
    "id": 14, 
    "items": [], 
    "name": "Visit the elderly"
  }, 
  {
    "created_by": 5, 
    "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
    "date_modified": null, 
    "description": "", 
    "id": 15, 
    "items": [], 
    "name": "Play new music"
  }
]

```

**Retrieve a Specific number of bucketlists**

You can retrieve a specified number of bucketlists. The server will respond with paginated response if possible, and provide additional metadata to retrieve more bucketlists. Make a GET request with a `limit` argument to `/api/bucketlists/?limit=<limit>` 

NOTE: The maximum number of bucketlist you can retrieve in a single page is 100.

See example below:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MTk5OTcsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIzNTk3fQ.eyJpZCI6NX0.JVNifJJqUZYkTVAW6cJD6aExXdkEMyO7r4NWlAJBm44"  -X GET  http://127.0.0.1:5000/api/bucketlists/\?limit=3

```

The server responds with:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 1156
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 20:43:12 GMT

{
  "data": [
    {
      "created_by": 5, 
      "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
      "date_modified": null, 
      "description": "", 
      "id": 3, 
      "items": [], 
      "name": "Build a House"
    }, 
    {
      "created_by": 5, 
      "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
      "date_modified": null, 
      "description": "", 
      "id": 4, 
      "items": [], 
      "name": "Plant 1000 tree seedlings"
    }, 
    {
      "created_by": 5, 
      "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
      "date_modified": null, 
      "description": "", 
      "id": 13, 
      "items": [], 
      "name": "Learn to cook"
    }
  ], 
  "meta": {
    "first": "http://127.0.0.1:5000/api/bucketlists/?page=1&limit=3", 
    "last": "http://127.0.0.1:5000/api/bucketlists/?page=2&limit=3", 
    "next": "http://127.0.0.1:5000/api/bucketlists/?page=2&limit=3", 
    "page": 1, 
    "pages": 2, 
    "per_page": 3, 
    "prev": null, 
    "total": 5
  }, 
  "urls": [
    "http://127.0.0.1:5000/api/bucketlists/3", 
    "http://127.0.0.1:5000/api/bucketlists/4", 
    "http://127.0.0.1:5000/api/bucketlists/13"
  ]
}

```

**Search for a Bucketlist by Name**

You can perform a full-text search for a bucketlist using part of its name. Make a GET request with a `q` argument to `/api/bucketlists/?q=<bucketlist_name>`. For instance:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MTk5OTcsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIzNTk3fQ.eyJpZCI6NX0.JVNifJJqUZYkTVAW6cJD6aExXdkEMyO7r4NWlAJBm44"  -X GET  http://127.0.0.1:5000/api/bucketlists/\?q\=ee

```

The server will respond with paginated response:

```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 578
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 20:48:47 GMT

{
  "data": [
    {
      "created_by": 5, 
      "date_created": "Sun, 29 Jan 2017 18:33:53 GMT", 
      "date_modified": null, 
      "description": "", 
      "id": 4, 
      "items": [], 
      "name": "Plant 1000 tree seedlings"
    }
  ], 
  "meta": {
    "first": "http://127.0.0.1:5000/api/bucketlists/?page=1&limit=20", 
    "last": "http://127.0.0.1:5000/api/bucketlists/?page=1&limit=20", 
    "next": null, 
    "page": 1, 
    "pages": 1, 
    "per_page": 20, 
    "prev": null, 
    "total": 1
  }, 
  "urls": [
    "http://127.0.0.1:5000/api/bucketlists/4"
  ]
}

```
		
**Create a Bucketlist Item**

To create an item in the bucketlist, make a POST request to the endpoint `/api/bucketlists/<id>/items/`, where `id`
 is the `id` of the bucketlist. One can only update the `name`, `priority` and `done` fields of an item.

 For instance:

 ```
 curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MTk5OTcsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzIzNTk3fQ.eyJpZCI6NX0.JVNifJJqUZYkTVAW6cJD6aExXdkEMyO7r4NWlAJBm44" -d '{"name":"Plant cyprus tree", "priority": "normal"}' -X POST  http://127.0.0.1:5000/api/bucketlists/4/items/
 
 ```

On successfully creating the item, the server responds with:

```
HTTP/1.0 201 CREATED
Content-Type: application/json
Location: http://127.0.0.1:5000/api/item/1
Content-Length: 45
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 20:54:46 GMT

{
  "message": "successfully created item"
}

```

**Update an Item in a Bucketlist**

To update an existing item, make a PUT request to the endpoint `/api/bucketlists/<id>/items/<item_id>/`, where `<id>`
 is the bucketlist id and `<item_id>` is the item id.

For instance:

```
 curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MjM3NjEsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzI3MzYxfQ.eyJpZCI6NX0.AI3xINj9r4_eDhQ8hiWSZsK2E4wo5U-kLYmtJn4R8Qo" -d '{"done": "true"}' -X PUT  http://127.0.0.1:5000/api/bucketlists/4/items/1

```

After successfully updating the Item, the server responds with:

```
HTTP/1.0 200 OK
Content-Type: application/json
Location: http://127.0.0.1:5000/api/item/1
Content-Length: 45
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 21:09:21 GMT

{
  "message": "item successfully updated"
}

```

**Deleting an Item**

To delete an item, make a DELETE request to the endpoint `/api/bucketlists/<id>/items/<item_id>/`, where `<id>` is the bucketlist id and `<item_id>` is the item id.

For instance:

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MjM3NjEsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzI3MzYxfQ.eyJpZCI6NX0.AI3xINj9r4_eDhQ8hiWSZsK2E4wo5U-kLYmtJn4R8Qo" -X DELETE  http://127.0.0.1:5000/api/bucketlists/4/items/1

```

The server responds with status code 204 to indicate successful deletion:

```
HTTP/1.0 204 NO CONTENT
Content-Type: application/json
Content-Length: 0
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 21:18:09 GMT

```

**Error handling**

Bucketlister tries to handle as many error cases as possible. In the event that one occurs, am appropriate error message in JSON format is returned. For example when one includes invalid data in a request body of a POST as :

```
curl -i -H "Content-Type: application/json" -H "Authorization: Bearer eyJpYXQiOjE0ODU3MjM3NjEsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDg1NzI3MzYxfQ.eyJpZCI6NX0.AI3xINj9r4_eDhQ8hiWSZsK2E4wo5U-kLYmtJn4R8Qo" -d '{"done": "true"}' -X POST  http://127.0.0.1:5000/api/bucketlists/4/items/ 

```

An error response is returned:

```
HTTP/1.0 400 BAD REQUEST
Content-Type: application/json
Content-Length: 108
Server: Werkzeug/0.11.15 Python/3.5.2
Date: Sun, 29 Jan 2017 21:23:41 GMT

{
  "error": "bad request", 
  "message": "invalid request: Item name must be provided", 
  "status": 400
}

```

