import logging
from menu_definitions import (
    add_employee, delete_employee, select_employee, print_employee,
    add_shift_date, delete_shift_date, select_shift_date, print_shift_date,
    add_shift, delete_shift, select_shift, print_shift,
    add_schedule, delete_schedule, select_schedule, print_schedule
)
from datetime import datetime

def main_menu():
    while True:
        print("\nHospital Shift Scheduling System")
        print("1. Add Employee")
        print("2. Delete Employee")
        print("3. View Employee")
        print("4. Add Shift Date")
        print("5. Delete Shift Date")
        print("6. View Shift Date")
        print("7. Add Shift")
        print("8. Delete Shift")
        print("9. View Shift")
        print("10. Schedule Employee")
        print("11. Delete Schedule")
        print("12. View Schedule")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            employee_id = int(input("Enter Employee ID: "))
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            add_employee(employee_id, first_name, last_name)

        elif choice == '2':
            employee_id = int(input("Enter Employee ID to delete: "))
            delete_employee(employee_id)

        elif choice == '3':
            employee_id = int(input("Enter Employee ID to view: "))
            employee = select_employee(employee_id)
            print_employee(employee)

        elif choice == '4':
            shift_date = input("Enter Shift Date (YYYY-MM-DD): ")
            holiday = bool(int(input("Is it a holiday? (1 for Yes, 0 for No): ")))
            # Parse the date
            shift_date = datetime.strptime(shift_date, "%Y-%m-%d").date()
            add_shift_date(shift_date, holiday)

        elif choice == '5':
            shift_date = input("Enter Shift Date to delete (YYYY-MM-DD): ")
            shift_date = datetime.strptime(shift_date, "%Y-%m-%d").date()
            delete_shift_date(shift_date)

        elif choice == '6':
            shift_date = input("Enter Shift Date to view (YYYY-MM-DD): ")
            shift_date = datetime.strptime(shift_date, "%Y-%m-%d").date()
            shift_date_obj = select_shift_date(shift_date)
            print_shift_date(shift_date_obj)

        elif choice == '7':
            shift_name = input("Enter Shift Name (e.g., Morning, Afternoon, Night): ")
            shift_start_hour = input("Enter Shift Start Time (HH:MM): ")
            shift_end_hour = input("Enter Shift End Time (HH:MM): ")
            shift_start_hour = datetime.strptime(shift_start_hour, "%H:%M").time()
            shift_end_hour = datetime.strptime(shift_end_hour, "%H:%M").time()
            add_shift(shift_name, shift_start_hour, shift_end_hour)

        elif choice == '8':
            shift_name = input("Enter Shift Name to delete: ")
            delete_shift(shift_name)

        elif choice == '9':
            shift_name = input("Enter Shift Name to view: ")
            shift = select_shift(shift_name)
            print_shift(shift)

        elif choice == '10':
            employee_id = int(input("Enter Employee ID: "))
            shift_date = input("Enter Shift Date (YYYY-MM-DD): ")
            shift_date = datetime.strptime(shift_date, "%Y-%m-%d").date()
            shift_name = input("Enter Shift Name (e.g., Morning, Afternoon, Night): ")
            add_schedule(employee_id, shift_date, shift_name)

        elif choice == '11':
            employee_id = int(input("Enter Employee ID for schedule deletion: "))
            shift_date = input("Enter Shift Date for schedule deletion (YYYY-MM-DD): ")
            shift_date = datetime.strptime(shift_date, "%Y-%m-%d").date()
            delete_schedule(employee_id, shift_date)

        elif choice == '12':
            employee_id = int(input("Enter Employee ID to view schedule: "))
            shift_date = input("Enter Shift Date to view schedule (YYYY-MM-DD): ")
            shift_date = datetime.strptime(shift_date, "%Y-%m-%d").date()
            schedule = select_schedule(employee_id, shift_date)
            print_schedule(schedule)

        elif choice == '0':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
