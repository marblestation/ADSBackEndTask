from ReferenceResolver import db
from datetime import datetime
from flask_restful import fields


class ResolveModel(db.Model):
    __tablename__ = 'resolve'
    id = db.Column(db.Integer, primary_key = True)
    refstring = db.Column(db.String(128))
    bibcode = db.Column(db.String(128))
    ip = db.Column(db.String(15), unique=False)
    creation_date = db.Column(db.DateTime)

    def __init__(self, **kwargs):
        super(ResolveModel, self).__init__(**kwargs)
        self.creation_date = datetime.utcnow()

    def __repr__(self):
        return '<Resolve %r>' % self.refstring

    resolve_marshaller = {
        'refstring': fields.String,
        'bibcode': fields.String,
    }

