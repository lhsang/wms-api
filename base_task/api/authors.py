from ..models import apiAuthor as api, author, db, Author
from flask_restplus import Resource, fields
import json
from ..helpers import JSONEncoder, resultToResponse
from ..services import authorSevice


@api.route('/')
class AuthorAPI(Resource):
    def get(self):
        result = authorSevice.getAllAuthors()
        return resultToResponse(result)

    @api.expect(author, validate=True)
    def post(self):
        result = authorSevice.createAuthor(api.payload)

        return resultToResponse(result)
