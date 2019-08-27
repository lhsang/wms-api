from ..models import db, Author, Book
from sqlalchemy import text


class AuthorService:
    def getAllAuthors(self):
        """
        find all authors
        :return: (True/False, status_code, {message, data}
        """
        try:
            authors = db.session.query(Author).all()
            return True, 200, {'message': 'Data found', 'data': authors}
        except Exception as e:
            print(str(e))
            return False, 400, {'message': 'Data not found'}

    def createAuthor(self, data):
        """
        create a author to author table
        :param data: api.payload
        :return: (True/False, status_code, {message, data}
        """
        try:
            newAuthor = Author(data)

            # check email and phone number format
            if not newAuthor.isValidEmail():
                raise Exception('Invalid email')

            if not newAuthor.isValidPhoneNumber():
                raise Exception('Invalid phone number')

            # save to db
            db.session.add(newAuthor)
            db.session.commit()
            return True, 200, {'message': 'Author created successfully', 'data': newAuthor}
        except Exception as e:
            return False, 400, {'message': str(e), "data": {}}

    def getAuthorWithHighestVote(self):
        try:
            authors = db.session.query(Author.id, Author.first_name, Author.last_name, Author.email, Author.phone,
                                       Author.book_count, Book.isbn, Book.title, Book.vote).from_statement(text('''
                                       SELECT * FROM author LEFT JOIN (SELECT DISTINCT ON ( a."authorID"	) 
                                       a.title, a.isbn, a."authorID", a.vote FROM book a LEFT JOIN book b ON 
                                       a."authorID" = b."authorID" AND a.vote < b.vote WHERE b."authorID" IS NULL) 
                                       max_vote ON author.id = max_vote."authorID"''')).all()
            listAuthors = []
            for x in authors:
                listAuthors.append({"id": x.id, "first_name": x.first_name, "last_name": x.last_name, "email": x.email,
                                    "phone": x.phone, "book_count": x.book_count, "isbn": x.isbn, "title": x.title,
                                    "vote": x.vote
                                    })
            return True, 200, {'message': 'Data found', 'data': listAuthors}
        except Exception as e:
            return False, 400, {'message': 'Data not found'}
