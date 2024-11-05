from sqlalchemy import Column, String, Time
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Shift(Base):
    __tablename__ = 'shift'

    shift_name = Column(String(20), primary_key=True)
    shift_start_hour = Column(Time, nullable=False)
    shift_end_hour = Column(Time, nullable=False)
