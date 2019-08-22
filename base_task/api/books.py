from ..models import book, apiBook as api
from flask_restplus import Resource


@api.route('/')
class BookAPI(Resource):
    def get(self):
        return {}

    @api.expect(book)
    def post(self):
        return {}