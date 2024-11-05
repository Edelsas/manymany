from sqlalchemy import Column, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ShiftDate(Base):
    __tablename__ = 'shift_date'

    shift_date = Column(Date, primary_key=True)
    holiday = Column(Boolean, nullable=False)
