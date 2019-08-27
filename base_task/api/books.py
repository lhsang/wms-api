from ..models import book, apiBook as api, Book, db
from flask_restplus import Resource
from ..helpers import JSONEncoder, resultToResponse
from ..services import bookService


@api.route('/')
class BookAPI(Resource):
    @api.doc(params={'title': 'Title of book', 'isbn': 'Book code'})
    def get(self):
        parser = api.parser()
        parser.add_argument('isbn').add_argument('title')
        args = parser.parse_args()
        status, code, data = bookService.getAllBooks(args)

        return resultToResponse([ status, code, data]), code

    @api.expect(book, validate=True)
    def post(self):
        data = api.payload
        status, code, data = bookService.createBook(data)
        return resultToResponse([ status, code, data]), code


@api.route('/<int:id>')
class BookAPIId(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Not found book'
    })
    def get(self, id):
        status, code, data = bookService.getOneBook(id)
        return resultToResponse([status, code, data]), code

    def delete(self, id):
        status, code, data = bookService.deleteBook(id)
        return resultToResponse([status, code, data]), code

    @api.expect(book)
    def put(self, id):
        status, code, data = bookService.editBook(id, api.payload)
        return resultToResponse([status, code, data]), code
