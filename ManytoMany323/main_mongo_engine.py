import mongoengine
from mongoengine import Document, StringField, IntField
from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.errors import PyMongoError
from pymongo.read_preferences import ReadPreference

"""
mongoengine.connect('Demonstration',
                    host='mongodb+srv://CECS-323-Spring-2024-User:relational>NoSQL@cluster0.uhlmij5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
"""
mongoengine.connect('Demonstration', host='mongodb://localhost:27017/Demonstration?replicaSet=rs0')

# Define your document classes
class User(Document):
    name = StringField(required=True)
    age = IntField(required=True)

class Order(Document):
    item = StringField(required=True)
    quantity = IntField(required=True)

if __name__ == "__main__":
    db = mongoengine.connection.get_db()
    # create two objects, one for each class to insert.  I have put a uniqueness
    # constraint on the item field in the Order class, so the first time this
    # insert is attempted (with no documents in the collection) it works.  After
    # that, the insert into order will fail.
    user_data = {'name': 'Alice', 'age': 28}
    order_data = {'item': 'Laptop', 'quantity': 1}
    with db.client.start_session() as session:
        # Start a transaction
        # The with construct guarantees us that session.commit_transaction for a normal
        # exit, and a session.abort_transaction() for an exit on an exception.
        with session.start_transaction(read_concern=ReadConcern('local'),
                                       write_concern=WriteConcern('majority')):
            try:
                # Perform your operations
                user = User(name=user_data['name'], age=user_data['age'])
                """
                Here is where things go south.  Python cheerfully allows me to pass
                an argument called 'session' in to the save method on Document, but
                the MongoEngine official documentation shows no such argument.  The
                net effect is that the save is not conducted in the context of a 
                session, so that if the item.save() aborts, there is no transaction
                to back out, and the user.save() action is never reversed.  ChatGPT
                conjectured that since MongoEngine is built on top of PyMongo, and 
                PyMongo supports sessions and transactions, that MongoEngine must
                also support sessions and transactions.  Alas, that is not so as 
                of 09/01/2024."""
                user.save(session=session)
                order = Order(item=order_data['item'], quantity=order_data['quantity'])
                order.save(session=session)
                #            error = 1 / 0  # force an exception to occur
                # If any exception occurs, the transaction will be aborted
                print("Transaction successful!")
            except Exception as e:
                print(f"Transaction failed: {e}")
    print('all done!')
