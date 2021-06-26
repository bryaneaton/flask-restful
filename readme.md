## Synopsis

A quick project i created while following Jose Salvatierra's excellent flask tutorial on Udemy. https://www.udemy.com/course/rest-api-flask-and-python/learn/lecture/6038434?start=0#overview

#### Start Postgres or SQL Server db and update credentials on `config.py`, SQL alchemy will create the database objects. 

#### Add user 
curl -d "username=user1&password=abcd" -X POST http://localhost:5000/register