from flask_restplus import Namespace, fields
from ..models import db
from datetime import datetime

MAX_LENGTH_ISBN = 64
MAX_LENGTH_TITLE = 1024

api = Namespace('books', description='Books related operation')

book = api.model('Book', {
    'id': fields.Integer(description='Autoincrease'),
    'title': fields.String(required=True, max_length=MAX_LENGTH_TITLE),
    'year': fields.Integer(required=True),
    'isbn': fields.String(required=True, max_length=MAX_LENGTH_ISBN),
    'authorID': fields.Integer(required=True, desciption='Must exist ID'),
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
    isbn = db.Column(db.String(MAX_LENGTH_ISBN), nullable=False, index=True)
    title = db.Column(db.String(MAX_LENGTH_TITLE), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer)
    view = db.Column(db.Integer)
    vote = db.Column(db.Integer)
    download = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now())
    updated = db.Column(db.DateTime, default=datetime.now())

    authorID = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

    # author = db.relationship('Author', backref='books')

    def __init__(self, obj):
        for c in self.__table__.columns:
            try:
                if c.name != 'id':
                    setattr(self, c.name, obj[c.name])
            except Exception as e:
                print(str(e))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def isValidYear(self):
        if datetime.now().year >= self.year > 0:
            return True
        return False

    def isValidISBN(self):
        return True
