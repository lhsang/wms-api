from ..models import book, apiBook as api, Book, db
from flask_restplus import Resource
from datetime import datetime


@api.route('/')
class BookAPI(Resource):
    @api.marshal_with(book)
    def get(self):
        books = db.session.query(Book).all()
        return books

    @api.expect(book, validate=True)
    def post(self):
        data = api.payload
        print(data)
        try:
            newAuthor = Book(data)
            print(newAuthor.as_dict())
            db.session.add(newAuthor)
            db.session.commit()
        except:
            api.abort(500, 'Can not create a book')
        return {'message': 'Success'}, 200


@api.route('/<int:id>')
class BookAPIId(Resource):
    @api.marshal_with(book)
    @api.doc(responses={
        200: 'Success',
        400: 'Author not found'
    })
    def get(self, id):
        try:
            _book = db.session.query(Book).filter(Book.id == id).one()
            return _book
        except:
            return api.abort(400, 'Author not found')

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
