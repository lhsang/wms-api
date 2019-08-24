from ..models import db, Author


class AuthorService:
    def getAllAuthors(self):
        try:
            authors = db.session.query(Author).all()
            return True, 200, {'message': 'Data found', 'data': authors}
        except:
            return False, 500, {'message': 'Data not found'}

    def createAuthor(self, data):
        try:
            newAuthor = Author(data)

            # check email and phone number format
            if not newAuthor.isValidEmail():
                return False, 400, {'message': 'Invalid email format'}
            if not newAuthor.isValidPhoneNumber():
                return False, 400, {'message': 'Invalid phone number'}

            # save to db
            db.session.add(newAuthor)
            db.session.commit()
            return True, 200, {'message': 'Author created successfully', 'data': newAuthor}
        except:
            return False, 500, {'message': 'Can not create author'}