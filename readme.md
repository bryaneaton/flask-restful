## Synopsis

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
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/user`

#### Add Item
`curl -XGET -d "store_id=1&price=2.309" \
 -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYyNDgyMDYyMSwianRpIjoiNjcwNWQ5NWQtMjU4YS00YWNmLWE4ZTEtOWNlMzI5MTAzYzczIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IntcImNoZWNrX3Bhc3N3b3JkXCI6IG51bGwsIFwiZmluZF9ieV9pZFwiOiBudWxsLCBcImZpbmRfYnlfdXNlcm5hbWVcIjogbnVsbCwgXCJpZFwiOiAzLCBcInBhc3N3b3JkXCI6IFwiYWJjZGVcIiwgXCJxdWVyeVwiOiBudWxsLCBcInF1ZXJ5X2NsYXNzXCI6IG51bGwsIFwicmVnaXN0cnlcIjogbnVsbCwgXCJzYXZlX3RvX2RiXCI6IG51bGwsIFwidXNlcm5hbWVcIjogXCJib29mXCJ9IiwibmJmIjoxNjI0ODIwNjIxLCJleHAiOjE2MjQ4MjE1MjF9.8o6shRYHjIeNQo2Bb0AAwORwtsm1lebL4U_aNpR-ztk" http://localhost:5000/item/xyz`
