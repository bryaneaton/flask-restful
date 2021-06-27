## Synopsis

A quick project i created while following Jose Salvatierra's excellent flask tutorial 
on Udemy. https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/6038434?start=0#overview

* Now updated with Flask 2.0 and Flask-Extended!

#### Start Postgres or SQL Server db and update credentials on `config.py`
* update `SQLALCHEMY_DATABASE_URI` in app.py with db config name
* SQL alchemy will create the database objects on app creation.

#### Add user 
`curl -d "username=user1&password=abcd" -X POST http://localhost:5000/register`