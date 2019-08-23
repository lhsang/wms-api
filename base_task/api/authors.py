from ..models import apiAuthor as api, author, db, Author
from flask_restplus import Resource, fields
import json
from ..helpers import JSONEncoder


@api.route('/')
class AuthorAPI(Resource):
    def get(self):
        authors = db.session.query(Author).all()
        return {'data': json.loads(json.dumps(authors, cls=JSONEncoder))}

    @api.expect(author, validate=True)
    def post(self):
        data = api.payload
        try:
            newAuthor = Author(data)

            # check email and phone number format
            if not newAuthor.isValidEmail() or not newAuthor.isValidPhoneNumber():
                return {'message': 'Email or phone number invalid'}, 400

            # save to db
            db.session.add(newAuthor)
            db.session.commit()
        except:
            api.abort(500, 'Can not create an author')
        return {'message': 'Success'}, 200
