from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False	# turns of flask's native sqlalchemy tracker becuause flask_sqlalchemy's is better
app.secret_key = 'aniket'
api = Api(app)

jwt = JWT(app, authenticate, identity)	# /auth

# alt/equivalent to @app.route()
api.add_resource(Item, '/item/<string:name>')	# localhost:5000/Aniket
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# to prevent the following from getting called on importing app.py
# it wil run only on python app.py
if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(debug=True)