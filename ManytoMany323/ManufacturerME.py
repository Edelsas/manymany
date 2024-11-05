from mongoengine import *


class Manufacturer(Document):
    """
    The first argument is the physical name of the column.  There's no need to 
    specify that name in this case since the column name defaults to being the
    same as the attribute name.  I just did it for demonstration purposes.
    The next argument dictates the datatype and length.
    THe next argument dictates that this attribute is mandatory.  It defaults to
    optional, just as it does in DDL if we were to create a table by hand.
    SQLAlchemy insists that every mapped entity have a primary key, so I gave it one."""
    name = StringField(db_name='name', required=True)
    """It would be good to make address an alternate key in the database so that we don't 
    ever have more than one manufacturer sharing the same address.  We'll do that 
    in meta soon."""
    address = StringField(db_name='manufacturer_address', required=True)

    """We don't strictly need an explicit constructor for these mapped entity classes.  But I 
    always like to define one just because, if there is no __init__ for the class, then 
    calling the inherited constructor requires that you use named parameters rather than 
    positional parameters.  That can get verbose."""
    def __init__(self, name: str, address: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.address = address

    """Every class needs a __str__ method.  We will use this rather crude approach to 
    displaying a class instance in several places in our main.py code."""
    def __str__(self):
        return f'Automobile manufacturer name:{self.name} located: {self.address}'
