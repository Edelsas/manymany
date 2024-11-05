import logging
from datetime import date

from pymongo.client_session import ClientSession
from menu_definitions import (menu_mainME, add_select, delete_select, list_select,
                              select_select, update_select, debug_select,
                              yes_no, transmission_type)
# Note that until you import your SQLAlchemy declarative classes, such as Manufacturer, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from ManufacturerME import Manufacturer
from CarModelME import CarModel
from Menu import Menu
from input_utilities import input_int_range, input_float_range
from CommandLogger import CommandLogger, log
from pymongo import monitoring
import logging
import mongoengine


"""This version is sample code for the same schema as is demonstrated in main.py, except this
one uses MongoEngine instead.  Because of that, there is no support for transactions as yet,
but I've elected to concentrate on the ODM aspects rather than the ACID/BASE elements of
MongoEngine."""


class Session(ClientSession):
    """I'm hoping to be able to actually use the Session in the transactions in this eventually,
    so I'm faking it here with this class definition."""
    pass

def menu_loop(menu: Menu, sess: Session):
    """Little helper routine to just keep cycling in a menu until the user signals that they
    want to exit.
    :param  menu:   The menu that the user will see.
    :param  sess:   The database connect session that the operation selected will use."""
    action: str = ''
    while action != menu.last_action():
        action = menu.menu_prompt()
        print('next action: ', action)
        exec(action)


def add(session: Session):
    """Top level menu prompt for any add operation."""
    menu_loop(add_select, session)


def list_members(session: Session):
    """Top level menu prompt for any list members operation."""
    menu_loop(list_select, session)


def select(session: Session):
    """Top level menu prompt for any select operation."""
    menu_loop(select_select, session)


def delete(session: Session):
    """Top level menu prompt for any delete operation."""
    menu_loop(delete_select, session)

def update(session: Session):
    """Top level menu prompt for any update operation."""
    menu_loop(update_select, session)

def add_manufacturer(session: Session):
    valid: bool = False
    while not valid:
        manufacturer_name = input("Enter manufacturer's name -->")
        manufacturer_address = input("Enter manufacturer's address -->")
        """
        Rather than perform two searches, one for any manufacturers with that name, and 
        a separate one for any manufacturers with that address, I look for any 
        manufacturers who match on either of those fields.  It's not very user-friendly
        because I cannot tell which (or both) of those duplicates an existing entry."""
        # The value of the $or key is a list of one or more criteria.
        # The value of the $match is a single criteria: the $or.
        # The pipeline overall has just one stage in it this time.
        pipeline = [
            {"$match":{"$or":[{"name": manufacturer_name},
                              {"address": manufacturer_address}]}}
        ]
        # Sadly, objects() has no count(), so we have to first turn the iterable returned
        # by PyMongo into a list, then get the number of elements in the list.
        manufacturer_count = len(list(Manufacturer.objects().aggregate(pipeline)))
        # At this point, we need to be aware of, and enforce the uniqueness constraints on
        # Manufacturer since we are not yet using the database for alternate keys.
        if manufacturer_count != 0:
            print('Error, we already have a manufacturer by that name and/or address.')
        else:
            valid = True
    manufacturer = Manufacturer(manufacturer_name, manufacturer_address)
    manufacturer.save()

def add_car_model(session: Session):
    """
    Create a new instance of CarModel in the database.
    :param session: The SQLAlchemy session that we are using.
    :return: None
    """
    valid: bool = False
    while not valid:
        manufacturer_name = select_manufacturer(session).name
        model_name = input("Enter the name of the model-->")
        current_date = date.today()
        current_year = current_date.year
        model_year = input_int_range("Enter the year of the model-->", 1914, current_year)
        print('For the next two prompts, put 0 if the vehicle is all EV.')
        fuel_economy_city = input_int_range("Enter the miles/gallon city-->", 10, 100)
        fuel_economy_hwy = input_int_range("Enter the miles/gallon highway-->", fuel_economy_city, 100)
        trani_type = transmission_type.menu_prompt()
        climate_control_zones = input_int_range("Enter the # of climate control zones-->", 1, 3)
        range_gasoline = input_int_range("Enter the range on gasoline (0 if all EV)-->", 0, 1000)
        range_elect = input_int_range("Enter the range on electricity (0 if all gasoline-->", 0, 1000)
        retailPrice = input_float_range("Enter the retail price-->", 1000, 500000)
        # Check to make sure that we are not violating the primary key of CarModel.
        pipeline = [
            {"$match": {"$and": [{"manufacturer_name": manufacturer_name},
                                 {"model_name": model_name},
                                 {"model_year": model_year}]}}
        ]
        car_model_count = len(list(CarModel.objects().aggregate(pipeline)))
        if car_model_count != 0:
            print('Error, we already have a car model with that name, year, & manufacturer.')
        else:
            valid = True
    car_model = CarModel(manufacturer_name, model_name, model_year, fuel_economy_city,
                         fuel_economy_hwy, trani_type, climate_control_zones, range_gasoline,
                         range_elect, retailPrice)
    car_model.save()

def delete_manufacturer(session: Session):
    ok: bool = False
    while not ok:
        manufacturer: Manufacturer = select_manufacturer(session)
        """Pathetically, the support for aggregation in PyMongo does not map from the 
        attribute names (manufacturerName in this case) to the physical field names
        in the document.  So I have to resort to using the physical names here."""
        pipeline = [
            {"$match": {"manufacturer_name": manufacturer.name}}
        ]
        # Sadly, objects() has no count(), so we have to first turn the iterable returned
        # by PyMongo into a list, then get the number of elements in the list.
        child_count: int = len(list(CarModel.objects().aggregate(pipeline)))

        if child_count > 0:
            print('Error, you cannot delete that manufacturer, there are Car Models that depend on it.')
        else:
            ok = True
    manufacturer.delete()

def delete_car_model(session: Session):
    car_model: CarModel = select_car_model(session)
    car_model.delete()

def select_manufacturer(session: Session) -> Manufacturer:
    found: bool = False
    manufacturer_name:str = ''
    while not found:
        manufacturer_name = input("Name of the manufacturer that you're looking for-->")
        pipeline = [
            {"$match": {"name": manufacturer_name}}
        ]
        # Sadly, objects() has no count(), so we have to first turn the iterable returned
        # by PyMongo into a list, then get the number of elements in the list.
        manufacturer_name_count = len(list(Manufacturer.objects().aggregate(pipeline)))

        if manufacturer_name_count != 0:
            found = True
        else:
            print ("That manufacturer could not be found.  Try again.")
    """
    MongoEngine returns an iterable of documents (Python dictionaries) from the aggregate 
    function.  But I need the actual object to operate on.  The document includes the _id 
    value, so I perform yet another query, but this time NOT using the aggregate pipeline,
    to return just the first object that comes back from looking for the manufacturer by 
    the _id value.  MongoDB makes sure that _id is always unique.  Note that MongoENGINE
    knows the _id field as just 'id'."""
    for manufacturer in Manufacturer.objects().aggregate(pipeline):
        return Manufacturer.objects(id=manufacturer.get('_id')).first()

def select_car_model(session: Session) -> CarModel:
    found: bool = False
    manufacturer_name:str = ''
    while not found:
        manufacturer = select_manufacturer(session)
        model = input(f"Enter the name of the model from manufacturer: {manufacturer.name}-->")
        current_date = date.today()
        current_year = current_date.year
        year = input_int_range("Enter the year of the model-->", 1914, current_year)

        pipeline = [
            {"$match": {"$and": [{"manufacturer_name": manufacturer.name},
                                 {"model_name": model},
                                 {"model_year": year}]}}
        ]
        car_model_count = len(list(CarModel.objects().aggregate(pipeline)))
        if car_model_count != 0:
            found = True
        else:
            print ("That car model could not be found.  Try again.")

    for car_model in CarModel.objects().aggregate(pipeline):
        return CarModel.objects(id=car_model.get('_id')).first()

def list_manufacturer(session: Session):
    manufacturers: [Manufacturer] = Manufacturer.objects().order_by('+name')
    for manufacturer in manufacturers:
        print(manufacturer.name)

def list_car_model(session: Session):
    car_models: [CarModel] = CarModel.objects().order_by(
        '+manufacturerName', '+modelName', '+modelYear')
    for car_model in car_models:
        print(car_model)

def update_manufacturer(session: Session):
    manufacturer = select_manufacturer(session)
    newName = input(f'Current name is: {manufacturer.name}.  Enter new name -->')
    pipeline = [
        {"$match": {"manufacturer_name": manufacturer.name}}
    ]
    child_count: int = len(list(CarModel.objects().aggregate(pipeline)))

    if child_count > 0:
        print('Error, you cannot update that manufacturer, there are Car Models that depend on it.')
    else:
        manufacturer.name = newName
        manufacturer.save()


if __name__ == '__main__':
    print('Starting in main.')

    monitoring.register(CommandLogger())
    mongoengine.connect('Demonstration', host='mongodb://localhost:27017/Demonstration?replicaSet=rs0')
    db = mongoengine.connection.get_db()
    """This actually initiates a session at the PyMongo layer of the software architecture, but
    I cannot get MongoEngine to actually use it.  So I'm paving the way to do that eventually 
    (since I'm hoping that MongoEngine eventually supports passing the Session in to the 
    save method) to be prepared, and to look as much like the SQLAlchemy code as I can."""
    sess: Session = db.client.start_session()
    main_action: str = ''
    while main_action != menu_mainME.last_action():
        main_action = menu_mainME.menu_prompt()
        print('next action: ', main_action)
        exec(main_action)
    log.info('All done for now.')
