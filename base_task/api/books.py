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
        result = bookService.getAllBooks(args)

        return resultToResponse(result)

    @api.expect(book, validate=True)
    def post(self):
        data = api.payload
        result = bookService.createBook(data)
        return resultToResponse(result)


@api.route('/<int:id>')
class BookAPIId(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Not found book'
    })
    def get(self, id):
        return resultToResponse(bookService.getOneBook(id))

    def delete(self, id):
        return resultToResponse(bookService.deleteBook(id))

    @api.expect(book)
    def put(self, id):
        return resultToResponse(bookService.editBook(id, api.payload))
