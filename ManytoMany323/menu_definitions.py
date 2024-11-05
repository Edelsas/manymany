from Menu import Menu
from Option import Option
from db_connection import session
from employee import Employee
from ShiftDate import ShiftDate
from Shift import Shift
from Schedule import Schedule
"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

def add_employee(employee_id, first_name, last_name):
    employee = Employee(employee_id=employee_id, first_name=first_name, last_name=last_name)
    session.add(employee)
    session.commit()
    print("Employee added.")

def delete_employee(employee_id):
    employee = session.query(Employee).filter_by(employee_id=employee_id).first()
    if employee:
        session.delete(employee)
        session.commit()
        print("Employee deleted.")
    else:
        print("Employee not found.")

def select_employee(employee_id):
    employee = session.query(Employee).filter_by(employee_id=employee_id).first()
    return employee

def print_employee(employee):
    if employee:
        print(f"Employee ID: {employee.employee_id}, Name: {employee.first_name} {employee.last_name}")
    else:
        print("Employee not found.")

# ShiftDate CRUD Functions
def add_shift_date(shift_date, holiday):
    shift_date_obj = ShiftDate(shift_date=shift_date, holiday=holiday)
    session.add(shift_date_obj)
    session.commit()
    print("ShiftDate added.")

def delete_shift_date(shift_date):
    shift_date_obj = session.query(ShiftDate).filter_by(shift_date=shift_date).first()
    if shift_date_obj:
        session.delete(shift_date_obj)
        session.commit()
        print("ShiftDate deleted.")
    else:
        print("ShiftDate not found.")

def select_shift_date(shift_date):
    shift_date_obj = session.query(ShiftDate).filter_by(shift_date=shift_date).first()
    return shift_date_obj

def print_shift_date(shift_date_obj):
    if shift_date_obj:
        print(f"Shift Date: {shift_date_obj.shift_date}, Holiday: {shift_date_obj.holiday}")
    else:
        print("ShiftDate not found.")

# Shift CRUD Functions
def add_shift(shift_name, shift_start_hour, shift_end_hour):
    shift = Shift(shift_name=shift_name, shift_start_hour=shift_start_hour, shift_end_hour=shift_end_hour)
    session.add(shift)
    session.commit()
    print("Shift added.")

def delete_shift(shift_name):
    shift = session.query(Shift).filter_by(shift_name=shift_name).first()
    if shift:
        session.delete(shift)
        session.commit()
        print("Shift deleted.")
    else:
        print("Shift not found.")

def select_shift(shift_name):
    shift = session.query(Shift).filter_by(shift_name=shift_name).first()
    return shift

def print_shift(shift):
    if shift:
        print(f"Shift Name: {shift.shift_name}, Start Hour: {shift.shift_start_hour}, End Hour: {shift.shift_end_hour}")
    else:
        print("Shift not found.")

# Schedule CRUD Functions
def add_schedule(employee_id, shift_date, shift_name):
    # Check if the nurse is already scheduled on that date
    existing_schedule = session.query(Schedule).filter_by(employee_id=employee_id, shift_date=shift_date).first()
    if existing_schedule:
        print("This employee is already scheduled on this date.")
        return

    schedule = Schedule(employee_id=employee_id, shift_date=shift_date, shift_name=shift_name)
    session.add(schedule)
    session.commit()
    print("Schedule added.")

def delete_schedule(employee_id, shift_date):
    schedule = session.query(Schedule).filter_by(employee_id=employee_id, shift_date=shift_date).first()
    if schedule:
        session.delete(schedule)
        session.commit()
        print("Schedule deleted.")
    else:
        print("Schedule not found.")

def select_schedule(employee_id, shift_date):
    schedule = session.query(Schedule).filter_by(employee_id=employee_id, shift_date=shift_date).first()
    return schedule

def print_schedule(schedule):
    if schedule:
        print(f"Employee ID: {schedule.employee_id}, Shift Date: {schedule.shift_date}, Shift Name: {schedule.shift_name}")
    else:
        print("Schedule not found.")
