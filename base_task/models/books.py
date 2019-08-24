from flask_restplus import Namespace, fields
from ..models import db
from datetime import datetime

api = Namespace('books', description='Books related operation')

book = api.model('Book', {
    'id': fields.Integer(description='Autoincrease'),
    'title': fields.String(required=True),
    'year': fields.Integer(required=True),
    'isbn': fields.String(required=True),
    'authorID': fields.Integer(required=True),
    'status': fields.Integer(default=1),
    'created': fields.DateTime(default=datetime.now()),
    'updated': fields.DateTime(default=datetime.now()),
    'view': fields.Integer(default=0),
    'vote': fields.Integer(default=0),
    'download': fields.Integer(default=0)
})


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)
    view = db.Column(db.Integer)
    vote = db.Column(db.Integer)
    download = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    authorID = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author')

    def __init__(self, obj):
        for c in self.__table__.columns:
            try:
                if c.name != 'id':
                    setattr(self, c.name, obj[c.name])
            except:
                print("An exception occurred")

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def isValidYear(self):
        if datetime.now().year >= self.year > 0:
                return True
        return False

    def isValidISBN(self):
        return True