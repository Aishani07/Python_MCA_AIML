
# INTEGRATED EXPENSE, ATTENDANCE, GRADING AND BILLING MANAGER

def student_details():

    print("=" * 45)
    print("Name     : Aishani Das")
    print("Roll No. : 2601940057")
    print("=" * 45)


expenses = []
attendance = []
students = []
bills = []

categories = ["Food", "Travel", "Shopping", "Education", "Other"]


# COMMON FUNCTIONS

def get_number(message):
    while True:
        try:
            number = float(input(message))
            if number >= 0:
                return number
            print("Please enter a positive number.")
        except:
            print("Please enter a valid number.")


def get_whole_number(message):
    while True:
        try:
            number = int(input(message))
            if number >= 0:
                return number
            print("Please enter a positive number.")
        except:
            print("Please enter a valid whole number.")


def get_name(message):
    while True:
        name = input(message).strip()
        if name != "" and name.replace(" ", "").isalpha():
            return name
        print("Name must contain only alphabets.")


def get_roll_no(message):
    while True:
        roll_no = input(message).strip()
        if roll_no.isdigit():
            return roll_no
        print("Roll number must be a non-negative whole number.")


def check_student(roll_no, name, records):
    for student in records:
        if student[0] == roll_no:
            print("Roll number already exists.")
            return False

        if student[1].lower() == name.lower():
            print("Student name already exists.")
            return False

    return True


# EXPENSE MANAGEMENT

def add_expense():
    student_details()
    print("\n--- Add Expense ---")

    name = get_name("Enter expense name: ")

    print("Categories:", categories)
    category = input("Enter category: ").title()

    if category not in categories:
        print("Invalid category. Using Other.")
        category = "Other"

    amount = get_number("Enter amount: ")

    expenses.append([name, category, amount])

    print("Expense added successfully!")


def expense_summary():
    student_details()
    print("\n--- Expense Summary ---")

    if len(expenses) == 0:
        print("No expenses found.")
        return

    total = 0

    for expense in expenses:
        total = total + expense[2]

    print("Total expenses:", total)

    for category in categories:
        category_total = 0

        for expense in expenses:
            if expense[1] == category:
                category_total = category_total + expense[2]

        print(category, ":", category_total)

    highest = expenses[0]
    lowest = expenses[0]

    for expense in expenses:
        if expense[2] > highest[2]:
            highest = expense

        if expense[2] < lowest[2]:
            lowest = expense

    print("Highest expense:", highest[0], "-", highest[2])
    print("Lowest expense:", lowest[0], "-", lowest[2])


def expense_menu():
    student_details()
    while True:
        print("\n--- Expense Management ---")
        print("1. Add Expense")
        print("2. View Expense Summary")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                add_expense()
            case "2":
                expense_summary()
            case "3":
                break
            case _:
                print("Invalid choice.")


# ATTENDANCE MANAGEMENT

def mark_attendance():
    student_details()
    print("\n--- Mark Attendance ---")

    while True:
        roll_no = get_roll_no("Enter roll number: ")
        name = get_name("Enter student name: ")

        if check_student(roll_no, name, attendance):
            break

    working_days = get_whole_number("Enter total working days: ")
    present_days = get_whole_number("Enter present days: ")

    if present_days > working_days:
        print("Present days cannot be greater than working days.")
        return

    if working_days == 0:
        percentage = 0
    else:
        percentage = (present_days / working_days) * 100

    if percentage >= 75:
        status = "Eligible"
    elif percentage >= 60:
        status = "Warning"
    else:
        status = "Shortage"

    attendance.append([
        roll_no, name, working_days,
        present_days, percentage, status
    ])

    print("Attendance recorded successfully!")


def attendance_summary():
    student_details()
    print("\n--- Attendance Summary ---")

    if len(attendance) == 0:
        print("No attendance records found.")
        return

    for student in attendance:
        print("\nRoll Number:", student[0])
        print("Name:", student[1])
        print("Working Days:", student[2])
        print("Present Days:", student[3])
        print("Attendance:", round(student[4], 2), "%")
        print("Status:", student[5])


def attendance_menu():
    student_details()
    while True:
        print("\n--- Attendance Management ---")
        print("1. Mark Attendance")
        print("2. View Attendance Summary")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                mark_attendance()
            case "2":
                attendance_summary()
            case "3":
                break
            case _:
                print("Invalid choice.")


# GRADING MANAGEMENT

def add_student():
    student_details()
    print("\n--- Add Student Marks ---")

    while True:
        roll_no = get_roll_no("Enter roll number: ")
        name = get_name("Enter student name: ")

        if check_student(roll_no, name, students):
            break

    print("Enter marks of 5 subjects separated by commas.")
    print("Example: 80,75,90,65,85")

    while True:
        try:
            marks = list(map(float, eval(input("Enter marks: "))))

            if len(marks) != 5:
                print("Please enter marks for exactly 5 subjects.")
            elif any(mark < 0 or mark > 100 for mark in marks):
                print("Marks must be between 0 and 100.")
            else:
                break

        except:
            print("Please enter marks in the correct format.")

    total = sum(marks)
    average = total / 5

    if any(mark < 35 for mark in marks):
        grade = "F"
        result = "Fail"
    elif average >= 90:
        grade = "A+"
        result = "Pass"
    elif average >= 80:
        grade = "A"
        result = "Pass"
    elif average >= 70:
        grade = "B"
        result = "Pass"
    elif average >= 60:
        grade = "C"
        result = "Pass"
    elif average >= 50:
        grade = "D"
        result = "Pass"
    else:
        grade = "E"
        result = "Pass"

    students.append([
        roll_no, name, marks, total,
        average, grade, result
    ])

    print("Student marks added successfully!")


def report_card():
    student_details()
    print("\n--- Student Report Card ---")

    if len(students) == 0:
        print("No student records found.")
        return

    roll_no = get_roll_no("Enter roll number: ")
    found = False

    for student in students:
        if student[0] == roll_no:
            found = True

            print("\nRoll Number:", student[0])
            print("Name:", student[1])
            print("Marks:", student[2])
            print("Total Marks:", student[3])
            print("Average:", round(student[4], 2))
            print("Grade:", student[5])
            print("Result:", student[6])

    if found == False:
        print("Student not found.")


def class_summary():
    student_details()
    print("\n--- Class Summary ---")

    if len(students) == 0:
        print("No student records found.")
        return

    total_average = 0
    passed = 0
    failed = 0

    for student in students:
        total_average = total_average + student[4]

        if student[6] == "Pass":
            passed = passed + 1
        else:
            failed = failed + 1

    class_average = total_average / len(students)

    print("Total Students:", len(students))
    print("Class Average:", round(class_average, 2))
    print("Students Passed:", passed)
    print("Students Failed:", failed)


def grading_menu():
    student_details()
    while True:
        print("\n--- Grading Management ---")
        print("1. Add Student Marks")
        print("2. View Report Card")
        print("3. View Class Summary")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                add_student()
            case "2":
                report_card()
            case "3":
                class_summary()
            case "4":
                break
            case _:
                print("Invalid choice.")


# BILLING MANAGEMENT

def create_bill():
    student_details()
    print("\n--- Create Bill ---")

    customer = get_name("Enter customer name: ")

    items = []
    subtotal = 0

    while True:
        item_name = get_name("Enter item name: ")
        price = get_number("Enter item price: ")
        quantity = get_whole_number("Enter quantity: ")

        item_total = price * quantity

        items.append([item_name, price, quantity, item_total])
        subtotal = subtotal + item_total

        choice = input("Add another item? (yes/no): ").lower()

        if choice != "yes":
            break

    if subtotal >= 5000:
        discount_rate = 15
    elif subtotal >= 3000:
        discount_rate = 10
    elif subtotal >= 1000:
        discount_rate = 5
    else:
        discount_rate = 0

    discount = subtotal * discount_rate / 100
    amount_after_discount = subtotal - discount
    tax = amount_after_discount * 18 / 100
    final_amount = amount_after_discount + tax

    bills.append([
        customer, items, subtotal,
        discount, tax, final_amount
    ])

    print("\n--- BILL ---")
    print("Customer:", customer)

    for item in items:
        print(item[0], "| Price:", item[1],
              "| Quantity:", item[2],
              "| Total:", item[3])

    print("Subtotal:", subtotal)
    print("Discount:", discount)
    print("Tax (18%):", tax)
    print("Final Amount:", final_amount)

    print("Bill created successfully!")


def view_bills():
    student_details()
    print("\n--- All Bills ---")

    if len(bills) == 0:
        print("No bills found.")
        return

    for bill in bills:
        print("\nCustomer:", bill[0])
        print("Subtotal:", bill[2])
        print("Discount:", bill[3])
        print("Tax:", bill[4])
        print("Final Amount:", bill[5])


def billing_menu():
    student_details()
    while True:
        print("\n--- Billing Management ---")
        print("1. Create Bill")
        print("2. View All Bills")
        print("3. Back to Main Menu")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                create_bill()
            case "2":
                view_bills()
            case "3":
                break
            case _:
                print("Invalid choice.")


# GENERAL REPORTS

def reports_menu():
    student_details()
    while True:
        print("\n--- Reports Menu ---")
        print("1. Expense Summary")
        print("2. Attendance Summary")
        print("3. Class Summary")
        print("4. View All Bills")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                expense_summary()
            case "2":
                attendance_summary()
            case "3":
                class_summary()
            case "4":
                view_bills()
            case "5":
                break
            case _:
                print("Invalid choice.")


# MAIN MENU

def main():
    student_details()
    while True:
        print("\n--- INTEGRATED MANAGEMENT SYSTEM ---")
        print("1. Expense Management")
        print("2. Attendance Management")
        print("3. Grading Management")
        print("4. Billing Management")
        print("5. Reports")
        print("6. Exit")

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                expense_menu()
            case "2":
                attendance_menu()
            case "3":
                grading_menu()
            case "4":
                billing_menu()
            case "5":
                reports_menu()
            case "6":
                print("Thank you for using the system!")
                break
            case _:
                print("Invalid choice. Please try again.")


# START PROGRAM

main()
