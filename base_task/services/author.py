from ..models import db, Author


class AuthorService:
    def getAllAuthors(self):
        """
        find all authors
        :return: (True/False, status_code, {message, data}
        """
        try:
            authors = db.session.query(Author).all()
            return True, 200, {'message': 'Data found', 'data': authors}
        except:
            return False, 500, {'message': 'Data not found'}

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
                return False, 400, {'message': 'Invalid email format'}
            if not newAuthor.isValidPhoneNumber():
                return False, 400, {'message': 'Invalid phone number'}

            # save to db
            db.session.add(newAuthor)
            db.session.commit()
            return True, 200, {'message': 'Author created successfully', 'data': newAuthor}
        except:
            db.session.rollback()
            return False, 500, {'message': 'Can not create author'}

    def increaseBookCount(self, id, value):
        """
        Increase book count when modify
        :param id: id of author (required)
        :param value: value to increase, default value=1
        """
        try:
            db.session.flush()
            author = db.session.query(Author).filter(Author.id==id).one()
            setattr(author, 'book_count', getattr(author, 'book_count')+value)

            db.session.flush()
            db.session.commit()
            print("increased")
        except:
            print("Can not increase book count")