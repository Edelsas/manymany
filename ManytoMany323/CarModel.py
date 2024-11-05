from decimal import Decimal

from orm_base import Base
from sqlalchemy import String, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column


class CarModel(Base):
    """A CarModel is a product that is offered for sale by a manufacturer.  An instance
    of a CarModel can be driven by one person at a time, on roads on land, and can convey
    a small number of passengers and a small quantity of luggage.  A CarModel cannot,
    by itself, actually DO anything.  It is just an item in a manufacturer's catalog."""
    __tablename__ = 'car_models'    # Defaults to the same name as the class.  Use naming standards.
    manufacturerName: Mapped[str] = mapped_column('manufacturer_name',
                                                  String(16), nullable=False, primary_key=True)
    modelName: Mapped[str] = mapped_column('model_name', String(20), nullable=False,
                                           primary_key=True)
    modelYear: Mapped[int] = mapped_column('model_year', Integer, nullable=False,
                                           primary_key=True)
    fuelEconomyCity: Mapped[int] = mapped_column('fuel_economy_city', Integer, nullable=False)
    fuelEconomyHwy: Mapped[int] = mapped_column('fuel_economy_hwy', Integer, nullable=False)
    # This could be validated using a migrated foreign key, or an enumeration.
    transmissionType: Mapped[str] = mapped_column('transmission_type', String(10), nullable=False)
    climateControlZones: Mapped[int] = mapped_column('climate_control_zones', Integer,
                                                     nullable=False)
    rangeGasoline: Mapped[int] = mapped_column('range_gasoline', Integer, nullable=False)
    rangeElectric: Mapped[int] = mapped_column('range_electric', Integer, nullable=False)
    MSRP: Mapped[float] = mapped_column('manufacturers_suggested_retail_price',
                                        DECIMAL(precision=10, scale=2), nullable=False)

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
