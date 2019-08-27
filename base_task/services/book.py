from ..models import Book, db, Author
from datetime import datetime


class BookService:
    def getAllBooks(self, args):
        query = db.session.query(Book)
        try:
            if args['isbn']:
                query = query.filter(Book.isbn == args['isbn'])

            if args['title']:
                q = "%{}%".format(args['title'])
                query = query.filter(Book.title.like(q))

            books = query.all()
            return True, 200, {'message': 'Data found', 'data': books}
        except Exception as e:
            print(str(e))
            return False, 400, {'message': 'Data not found'}

    def getOneBook(self, id):
        try:
            _book = db.session.query(Book).filter(Book.id == id).one()
            return True, 200, {'message': 'Book found', 'data': _book}
        except Exception as e:
            print(str(e))
            return False, 400, {'message': 'Book not found', 'data': {}}

    def createBook(self, data):
        try:
            newBook = Book(data)

            if not newBook.isValidYear():
                raise Exception("Invalid year")

            db.session.add(newBook)
            db.session.commit()
            return True, 200, {'message': 'Book created successfully', 'data': newBook}
        except Exception as e:
            return False, 400, {'message': str(e), 'data': {}}

    def deleteBook(self, id):
        book = db.session.query(Book).get(id)
        if book:
            status = db.session.delete(book)
            db.session.commit()
            if status == 0:
                return False, 400, {'message': 'Book not found'}

            return True, 200, {'message': 'Book deleted successfully', 'data': {}}
        return False, 400, {'message': 'Book not found'}

    def editBook(self, id, data):
        change_attr = ['title', 'isbn', 'year', 'status', 'view', 'vote', 'download', 'authorID']

        try:
            _book = db.session.query(Book).get(id)

            if 'authorID' in data:
                author = db.session.query(Author).get(data['authorID'])
                if not author:
                    raise Exception(f'AuthorID = {data["authorID"]} not exist')

            # copy data
            for att in change_attr:
                try:
                    if data.get(att):
                        setattr(_book, att, data.get(att))
                except Exception as e:
                    print(str(e))

            setattr(_book, 'updated', datetime.now())

            # valid data
            if not _book.isValidYear():
                raise Exception('Invalid year')

            db.session.commit()
            return True, 200, {'message': 'Book edited successfully', 'data': _book}
        except Exception as es:
            db.session.rollback()
            return False, 400, {'message': str(es), 'data': {}}
