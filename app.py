import pyodbc
from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList
from security import authenticate, identity


# params = urllib.quote_plus("DRIVER={SQL Server Native Client 11.0};SERVER=CTG-SQLLAB01>;DATABASE=CTG_Custom;UID=dsuser;PWD=dsu3r_123;driver=[SQL Server]")
# SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # SQL lite connection string
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://dsuser:dsu3r_123@CTG-SQLLAB01:1433/ITQ?driver=SQL+Server+Native+Client+10.0" #SQL Server Credentials
# TODO: Add Postgres SQL Example

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # Auto Creates /auth endpoint

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db  #Avoid circular import
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True

