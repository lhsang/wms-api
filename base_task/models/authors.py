from flask_restplus import Namespace, fields
from ..models import db
from datetime import datetime

api = Namespace('authors', description='Authors related operation')

author = api.model('Author', {
    'id': fields.Integer(readOnly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'status': fields.Integer(default=1),
    'created': fields.DateTime(default=datetime.now()),
    'updated': fields.DateTime(default=datetime.now())
})


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)
    status = db.Column(db.Integer, default=1)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())
    book = db.relationship('Book')

    def __init__(self, obj):
        for c in self.__table__.columns:
            try:
                if c.name != 'id':
                    setattr(self, c.name, obj[c.name])
            except:
                print("An exception occurred")

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
