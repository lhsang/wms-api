from ..models import apiAuthor as api, author
from flask_restplus import Resource
from ..helpers import resultToResponse, setAssociationToResponse
from ..services import authorSevice


@api.route('/')
class AuthorAPI(Resource):
    def get(self):
        status, code, data = authorSevice.getAuthorWithHighestVote()
        res = resultToResponse([status, code, data])
        return res, code

    @api.expect(author, validate=True)
    def post(self):
        status, code, data = authorSevice.createAuthor(api.payload)

        return resultToResponse([status, code, data]), code
