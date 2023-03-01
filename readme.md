
A quick project i created while following Jose Salvatierra's excellent flask tutorial 
on Udemy. https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/6038434?start=0#overview

✨ Now updated with Flask 2.0 and Flask-Extended!!  ✨

### Start Postgres or SQL Server db and update credentials on `config.py`
* update `SQLALCHEMY_DATABASE_URI` in app.py with db config name
* SQL alchemy will create the database objects on app creation.


### Example endpoints
#### Add user 
`curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username": "luna", "password": "badgirl"}'`

#### Login
###### _`(Returns Auth Token)`_
`curl -X POST http://localhost:5000/user -H "Content-Type: application/json" -d '{"username": "luna", "password": "badgirl"}'`

### Grab token in variable
`export JWT=$(curl -s -X POST http://localhost:5000/user -H "Content-Type: application/json" -d @creds.json | jq .access_token)`

#### Add Store
###### _`(Replace with Auth Token)`_
`curl -X POST http://localhost:5000/store/xyz -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" -H "Accepts: application/json" `

### Add Item
`curl -X POST http://localhost:5000/item/apple -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" -H "Accepts: application/json" -d '{"store_id": 1, "price": "2.40"}'`
