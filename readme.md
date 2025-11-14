# Flask RESTful API

![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen)
![Tests](https://img.shields.io/badge/tests-62%20passed-brightgreen)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-3.1.2-blue)

A quick project i created while following Jose Salvatierra's excellent flask tutorial
on Udemy. https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/6038434?start=0#overview

✨ Now updated with Flask 3.1 and Flask-JWT-Extended 4.7!!  ✨

## Quick Start

### Start the Server

Use the provided `run.sh` script for easy server management:

```bash
# Start with SQLite (easiest for development)
./run.sh --sqlite

# Start with PostgreSQL (production)
./run.sh

# Install dependencies and start with tests
./run.sh --install-deps --run-tests --sqlite

# Custom port and host
./run.sh --sqlite --port 8080 --host 127.0.0.1

# Show all options
./run.sh --help
```

### Using the API Client

Use the `api-client.sh` helper script to interact with the API:

```bash
# Register a new user
./api-client.sh register john password123

# Login and save token
TOKEN=$(./api-client.sh login john password123 | jq -r '.access_token')

# Create a store
./api-client.sh --token "$TOKEN" create-store "Electronics"

# Create an item
./api-client.sh --token "$TOKEN" create-item "Laptop" 999.99 1

# List all items
./api-client.sh --token "$TOKEN" list-items

# Show all commands
./api-client.sh --help
```

## Running Tests

The project includes a comprehensive test suite with 96% code coverage.

```bash
# Install dependencies
pip install -r app/requirements.txt

# Run all tests
pytest tests/

# Run tests with coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_models.py -v
```

## Manual Setup

### Start Postgres or SQL Server db and update credentials on `config.py`
* update `SQLALCHEMY_DATABASE_URI` in app.py with db config name
* SQL alchemy will create the database objects on app creation.


## Example endpoints
#### Add user 
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/register`

#### Login
###### _`(Returns Auth Token)`_
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/user`

#### Add Item
###### _`(Replace with Auth Token)`_
`curl -XGET -d "store_id=1&price=2.309" \
 -H "Authorization: Bearer paste_token_here http://localhost:5000/item/xyz`
