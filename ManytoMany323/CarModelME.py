from decimal import Decimal

from mongoengine import*

class CarModel(Document):
    """A CarModel is a product that is offered for sale by a manufacturer.  An instance
    of a CarModel can be driven by one person at a time, on roads on land, and can convey
    a small number of passengers and a small quantity of luggage.  A CarModel cannot,
    by itself, actually DO anything.  It is just an item in a manufacturer's catalog."""
    manufacturerName = StringField(db_field='manufacturer_name', required=True)
    modelName = StringField(db_field='model_name', required=True)
    modelYear = IntField(db_field='model_year', required=True)
    fuelEconomyCity = IntField(db_field='fuel_economy_city', required=True)
    fuelEconomyHwy = IntField(db_field='fuel_economy_highway', required=True)
    # This could be validated using a migrated foreign key, or an enumeration.
    transmissionType = StringField(db_field='transmission_type', required=True)
    climateControlZones = IntField(db_field='climate_control_zones', required=True)
    rangeGasoline = IntField(db_field='range_gasoline', required=True)
    rangeElectric = IntField(db_field='range_electric', required=True)
    MSRP = DecimalField(db_field='manufacturers_suggested_retail_price',
                        required=True, precision=2,
                        rounding='ROUND_HALF_UP')

    # stipulate the name of the collection for this class.
    meta = {'collection': 'car_models'}

    def __init__(self, manufacturerName: str, modelName: str, modelYear: int,
                 fuelEconomyCity: int, fuelEconomyHwy: int, transmissionType: str,
                 climateControlZones: int, rangeGasoline: int, rangeElectric: int,
                 MSRP: Decimal, **kwargs):
        super().__init__(**kwargs)
        self.manufacturerName = manufacturerName
        self.modelName = modelName
        self.modelYear = modelYear
        self.fuelEconomyCity = fuelEconomyCity
        self.fuelEconomyHwy = fuelEconomyHwy
        self.transmissionType = transmissionType
        self.climateControlZones = climateControlZones
        self.rangeGasoline = rangeGasoline
        self.rangeElectric = rangeElectric
        self.MSRP = MSRP

    def __str__(self):
        return f'Automobile model name:{self.modelName} model year: {self.modelYear} manufacturer: {self.manufacturerName}'
