import os
from flask import Flask, request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from ReferenceResolver.Common.DataBase import init_db

app = Flask(__name__)
db_filename = "resolve.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+db_filename
app.config['SECRET_KEY'] = 'z3%kr3t66_ads21/*_k3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

#-------------------------------------------------------------------------------
db = SQLAlchemy(app)
if not os.path.exists("ReferenceResolver/"+db_filename):
    init_db(db) # WARNING: This action erases previous data in the database
#-------------------------------------------------------------------------------

from Resources import Resolve

api.add_resource(Resolve,  '/resolve/<string:refstring>', endpoint='resolve')
