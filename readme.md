
A quick project i created while following Jose Salvatierra's excellent flask tutorial 
on Udemy. https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/6038434?start=0#overview

✨ Now updated with Flask 2.0 and Flask-Extended!!  ✨

### Start Postgres or SQL Server db and update credentials on `config.py`
* update `SQLALCHEMY_DATABASE_URI` in app.py with db config name
* SQL alchemy will create the database objects on app creation.


### Example endpoints
#### Add user 
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/register`

#### Login
###### _`(Returns Auth Token)`_
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/user`

#### Add Item
###### _`(Replace with Auth Token)`_
`curl -XGET -d "store_id=1&price=2.309" \
 -H "Authorization: Bearer paste_token_here http://localhost:5000/item/xyz`
