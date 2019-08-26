from ..models import Book, Author, db
from sqlalchemy import event


# register events for Book table
@event.listens_for(Book, "after_insert")
@event.listens_for(Book, "after_delete")
def onCreateBook(target, connection, value):
    try:
        authorID = value.to_dict()['authorID']
        count = db.session.query(Book).filter(Book.authorID == authorID).count()
        connection.execute(f'update author set book_count = {count} where id ={authorID}')
    except Exception as e:
        print(str(e))


@event.listens_for(Book, "before_update")
def onUpdateBookAuthorID(mapper, connection, target):
    state = db.inspect(target)
    changes = {}
    for attr in state.attrs:
        hist = state.get_history(attr.key, True)
        if not hist.has_changes():
            continue
        old_value = hist.deleted[0] if hist.deleted else None
        new_value = hist.added[0] if hist.added else None
        changes[attr.key] = [old_value, new_value]
    try:
        if changes['authorID']:
            connection.execute(f'update author set book_count = book_count-1 where id ={changes["authorID"][0]}')
            connection.execute(f'update author set book_count = book_count+1 where id ={changes["authorID"][1]}')
    except Exception as e:
        print(str(e))
