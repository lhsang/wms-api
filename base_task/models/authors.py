from flask_restplus import Namespace, fields
from ..models import db
from datetime import datetime
import re

MAX_LENGTH_NAME = 32
MAX_LENGTH_EMAIL = 64
MAX_LENGTH_PHONE_NUMBER = 10
MAX_LENGTH_ADDRESS = 512

api = Namespace('authors', description='Authors related operation')

author = api.model('Author', {
    'id': fields.Integer(readOnly=True, description='Autoincrease'),
    'first_name': fields.String(required=True, max_length=MAX_LENGTH_NAME),
    'last_name': fields.String(required=True, max_length=MAX_LENGTH_NAME),
    'email': fields.String(description='Example: John.Smith@example.com', max_length=MAX_LENGTH_EMAIL),
    'phone': fields.String(description='Start with 0 and include 10 digits. EX:0987654321',
                           max_length=MAX_LENGTH_PHONE_NUMBER),
    'address': fields.String(max_length=MAX_LENGTH_ADDRESS),
    'status': fields.Integer(default=1),
    'created': fields.DateTime(default=datetime.now()),
    'updated': fields.DateTime(default=datetime.now())
})


class Author(db.Model):
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(MAX_LENGTH_NAME), nullable=False)
    last_name = db.Column(db.String(MAX_LENGTH_NAME), nullable=False)
    email = db.Column(db.String(MAX_LENGTH_EMAIL))
    phone = db.Column(db.String(MAX_LENGTH_PHONE_NUMBER))
    address = db.Column(db.String(MAX_LENGTH_ADDRESS))
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

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    def isValidEmail(self):
        patternEmail = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        if self.email:
            if re.match(patternEmail, self.email):
                return True
        else:
            # if email empty
            return True
        return False

    def isValidPhoneNumber(self):
        patternPhone = "(0\d{9}$)"
        if self.phone:
            if re.match(patternPhone, self.phone):
                return True
        else:
            return True
        return False
