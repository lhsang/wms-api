from ..models import apiAuthor as api, author, db, Author
from flask_restplus import Resource, fields


@api.route('/')
class AuthorAPI(Resource):
    @api.marshal_with(author)
    def get(self):
        authors = db.session.query(Author).all()
        return authors

    @api.expect(author, validate=True)
    @api.doc('Add an author')
    def post(self):
        data = api.payload
        try:
            newAuthor = Author(data)
            db.session.add(newAuthor)
            db.session.commit()
        except:
            api.abort(500, 'Can not create an author')
        return {'message': 'Success'}, 200

