from flask_restplus import Namespace, fields

api = Namespace('authors', description='Authors related operation')

author = api.model('Author', {
    'id': fields.Integer,
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'status': fields.Integer,
    'created': fields.DateTime,
    'updated': fields.DateTime
})
