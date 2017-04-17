#!/usr/bin/python
import json
from collections import Counter
from itertools import chain
from os.path import isfile
from sys import argv


def main():
    employees = []
    file_name = None
    added = False

    if len(argv) > 1:
        if isfile(argv[1]):
            file_name = argv[1]
    elif isfile("employees.json"):
        file_name = "employees.json"

    with open(file_name, 'r') as f:
        employees = json.load(f)

    while True:
        choice = raw_input("Do you want to add new employee (y/n): ").lower()
        if choice == 'n':
            break
        elif not choice == 'y':
            print "only 'y' or 'n'"
            continue

        add_employee(employees)
        added = True

    if added:
        if not file_name:
            file_name = "employees.json"
        with open(file_name, 'w') as f:
            json.dump(employees, f, indent=4)

    display_all_employees(employees)
    display_common_numbers(employees)

    return 0


def add_employee(employees):
    employee = {}
    employee['first_name'] = raw_input("\nEnter your first name: ")
    employee['last_name'] = raw_input("Enter your last name: ")
    employee['numbers'] = []
    for i in range(5):
        input_str = "select {0}st # (1 thru 69 excluding {1}): ".format(
            i + 1, ", ".join(str(e) for e in employee['numbers'])
        )

        if not employee['numbers']:
            input_str = "select 1st # (1 thru 69): "

        while True:
            try:
                input_num = int(raw_input(input_str))
            except ValueError:
                print "That is not integer!"
                continue
            if 1 > input_num > 69:
                print "The number can be chosen only between 1 and 69"
                continue
            employee['numbers'].append(input_num)
            break

    while True:
        try:
            employee['powerball'] = int(
                raw_input("select Power Ball # (1 thru 26): ")
            )
        except ValueError:
            print "That is not integer!"
            continue
        if 1 > employee['powerball'] > 26:
            print "The number can be chosen only between 1 and 26"
            continue
        break

    employees.append(employee)


def display_all_employees(employees):
    print '\n' + '\n'.join("{0} {1} {2} Powerball: {3}".format(
        employee['first_name'],
        employee['last_name'],
        ' '.join(str(num) for num in employee['numbers']),
        employee['powerball']
    ) for employee in employees)


def display_common_numbers(employees):
    print "\nPowerball winning number:"
    print "{0} Powerball: {1}".format(
        ' '.join(str(ordered_num[0]) for ordered_num in Counter(
            num for employee in employees for num in employee['numbers']
        ).most_common(5)),
        Counter(employee['powerball']
                for employee in employees).most_common(1)[0][0]
    )

if __name__ == "__main__":
    # start_time = time.time()
    main()
    # print("\n%s seconds" % (time.time() - start_time))
