# 🤖 Order API

## 📝 Project Structure

This Django project implement a RESTful `/orders/` endpoint that supports only the POST
HTTP Method. You can use this endpoint to create orders in the most forgiving market
ever: your imagination. See [Installation](#installation) to learn how to set up this
project and then check out [Running the Application](#running-the-application)
to find out what you can do!

## Installation

### Prerequisites

It is highly recommended to create and activate a python virtualenvironment of your
choice before you install/run this project. I personally like
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv).

### Setup

Install all project requirements and apply the migrations necessery to run the app with:

```
make install
```

## Running the Application

### Running the Endpoint

Bring up the `/orders/` endpoint at http://localhost:8000/orders/ with:

```
make app
```

### Making a request

With the `/orders/` endpoint up and running, make a request to http://localhost:8000/orders/
using your client of choice. Below are two samples for curl and requests (python). For more
details on the endpoint and the expected request payload structure, see
[Running the OpenAPI/Swagger view](#running-the-openAPI/Swagger-view).

```
# curl
curl --request POST \
  --url http://localhost:8000/orders/ \
  --header 'Content-Type: application/json' \
  --data '{
  "isin": "US88160R1014",
  "valid_until": "2147483647",
	"quantity": "1",
  "side": "buy",
	"limit_price": 1.11
}'
```

```
# requests
import requests

url = "http://localhost:8000/orders/"

payload = {
    "isin": "US88160R1014",
    "valid_until": "2147483647",
    "quantity": "1",
    "side": "buy",
    "limit_price": 1.11
}
headers = {
    "Content-Type": "application/json",
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

### Running Tests

To run all tests, simply:

```
make test
```

### Running the Demo

To run the demo application and get a feeling for the unlimited power at the tip of
your fingers, exectute the following two commands:

```
# Keep me running in one shell
make app

# Run me concurrently in a different shell
make demo
```

### Running the OpenAPI/Swagger view

To check out the OpenAPI/Swagger Endpoint docs, run:

```
make swagger
```

and go to http://localhost:8000
