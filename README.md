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





