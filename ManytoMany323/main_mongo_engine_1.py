import mongoengine
from mongoengine import Document, StringField, IntField
from menu_definitions import (menu_main_mongo, add_select, delete_select, list_select,
                              select_select, update_select, debug_select,
                              yes_no, transmission_type)
from Menu import Menu

"""
This is based on main_mongo_engine, but using transactions in a loop in the main, rather than 
inside a function.  It's definitely a prototype at this point.  As of 09/01/2024, this does not
work in that it does not actually enter the inserts into a session.  The only way to get 
sessions to work is to abandon MongoEngine and interface directly to PyMongo."""

# Define your document classes
class User(Document):
    name = StringField(required=True)
    age = IntField(required=True)

class Order(Document):
    item = StringField(required=True)
    quantity = IntField(required=True)

def create_user_and_order(user_data, order_data, session):
    user = User(name=user_data['name'], age=user_data['age'])
    user.save(session=session)

    order = Order(item=order_data['item'], quantity=order_data['quantity'])
    order.save(session=session)

def add(sess):
    user_data = {'name': 'Alice', 'age': 28}
    order_data = {'item': 'Laptop', 'quantity': 1}
    create_user_and_order(user_data, order_data, sess)

if __name__ == "__main__":
    print('Starting in main')
    mongoengine.connect('Demonstration',
                        host='mongodb+srv://CECS-323-Spring-2024-User:relational>NoSQL@cluster0.uhlmij5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    main_action: str = ''    # Start a client session
    db = mongoengine.connection.get_db()
    # start a transaction
    with db.client.start_session() as sess:
        while main_action != menu_main_mongo.last_action():
            # Start a transaction
            xactn_end: bool = False
            with sess.start_transaction():
                while main_action != menu_main_mongo.last_action() and not xactn_end:
                    main_action = menu_main_mongo.menu_prompt()
                    print(f'next action: {main_action}')
                    if main_action == 'sess.commit()' or main_action == 'sess.abort()':
                        xactn_end = True
                    exec(main_action)
