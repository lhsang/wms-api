from ..models import Book, Author, db
from sqlalchemy import event

# events for Book table
@event.listens_for(Book, "before_delete")
@event.listens_for(Book, "after_insert")
def onCreateBook(target, connection, value):
    print("Ssssssssssss")
    try:
        authorID = value.to_dict()['authorID']
        count = db.session.query(Book).filter(Book.authorID == authorID).count()
        print(count)
        connection.execute(f'update author set book_count = {count} where id ={authorID}')
    except:
        print(f"Can not update book count for authorID={authorID}")
