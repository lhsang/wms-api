from ..models import book, apiBook as api, Book, db
from flask_restplus import Resource
from datetime import datetime
import json
from ..helpers import JSONEncoder


@api.route('/')
class BookAPI(Resource):
    @api.doc(params={'title': 'Title of book', 'isbn': 'Book code'})
    def get(self):
        parser = api.parser()
        parser.add_argument('isbn').add_argument('title')
        args = parser.parse_args()

        query = db.session.query(Book)
        try:
            if args['isbn']:
                query = query.filter(Book.isbn == args['isbn'])

            if args['title']:
                q = "%{}%".format(args['title'])
                query = query.filter(Book.title.like(q))
        except: pass

        books = query.all()
        return {'data': json.loads(json.dumps(books, cls=JSONEncoder))}

    @api.expect(book, validate=True)
    def post(self):
        data = api.payload
        try:
            newBook = Book(data)
            if not newBook.isValidYear():
                return {'message': 'Year is invalid'}, 400
            db.session.add(newBook)
            db.session.commit()
        except:
            api.abort(500, 'Can not create a book')
        return {'message': 'Success'}, 200


@api.route('/<int:id>')
class BookAPIId(Resource):
    @api.doc(responses={
        200: 'Success',
        400: 'Not found book'
    })
    def get(self, id):
        try:
            _book = db.session.query(Book).filter(Book.id == id).one()
            return {'data': json.loads(json.dumps(_book, cls=JSONEncoder))}
        except:
            return api.abort(400, 'Not found book')

    def delete(self, id):
        status = db.session.query(Book).filter(Book.id == id).delete()
        if status == 0:
            api.abort(400, "Book not found")
        return {'message': 'Deleted book id = %i' % id}

    @api.expect(book, validate=True)
    def put(self, id):
        change_attr = ['title', 'isbn', 'year', 'status', 'view', 'vote', 'download']

        data = api.payload
        try:
            _book = db.session.query(Book).filter(Book.id == id).one()

            for att in change_attr:
                try:
                    if data.get(att):
                        setattr(_book, att, data.get(att))
                except: pass

            setattr(_book, 'updated', datetime.now())

            db.session.flush()
            db.session.commit()
            return {'message': 'Success'}
        except:
            api.abort(400, "Book not found")
