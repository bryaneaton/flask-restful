from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from config import postgresqlConfig
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Dese.Decent.Pups.BOOYO0OST'
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

