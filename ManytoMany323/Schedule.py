from sqlalchemy import Column, Integer, Date, String, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Schedule(Base):
    __tablename__ = 'schedule'

    employee_id = Column(Integer, ForeignKey('employee.employee_id'), nullable=False)
    shift_date = Column(Date, ForeignKey('shift_date.shift_date'), nullable=False)
    shift_name = Column(String(20), ForeignKey('shift.shift_name'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('employee_id', 'shift_date'),
    )
