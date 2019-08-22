from flask_restplus import Namespace, fields

api = Namespace('books', description='Books related operation')

book = api.model('book', {
    'id': fields.Integer,
    'title': fields.String(required=True),
    'year': fields.Integer(required=True),
    'authorID': fields.Integer,
    'status': fields.Integer,
    'created': fields.DateTime,
    'updated': fields.DateTime,
    'view': fields.Integer,
    'vote': fields.Integer,
    'download': fields.Integer
})
