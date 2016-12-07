from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from ReferenceResolver.Common.DataBase import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resolve.db'
app.config['SECRET_KEY'] = 'z3%kr3t66_ads21/*_k3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

#-------------------------------------------------------------------------------
db = SQLAlchemy(app)
init_db(db)
#-------------------------------------------------------------------------------

from Resources import Resolve

api.add_resource(Resolve,  '/resolve/<string:refstring>', endpoint='resolve')
