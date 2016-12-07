from flask import request
from flask import g # Request context reserved for custom data
from flask_restful import Resource, marshal_with
from ReferenceResolver import db
from ReferenceResolver.Models import ResolveModel

class Resolve(Resource):

    #@marshal_with(ResolveModel.resolve_marshaller)
    def get(self, refstring):
        #user = UserModel.query.get(user_id)
        #return user
        #return '', 204
        #return {answer_id: answer.text}
        return {'refstring': refstring, 'bibcode': "TODO"}
