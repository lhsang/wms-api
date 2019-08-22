from ..models import apiAuthor as api, author
from flask_restplus import Resource


@api.route('/')
class AuthorAPI(Resource):
    def get(self):
        return {}

    @api.expect(author, validate=True)
    @api.doc('Add an author')
    def post(self):
        return {}
