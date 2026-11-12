"""Entry point and main menu for the Student Result Management System."""

import re
from datetime import datetime

from student import Student
from results import (
    SUBJECTS,
    calculate_total,
    calculate_average,
    get_grade,
    get_class_position,
    sort_by_average,
    sort_by_name,
)
from storage import load_students, save_students
from reports import (
    print_student_table,
    print_report_card,
    print_statistics,
    save_text_report,
    export_csv,
)

ID_PATTERN = r"^[A-Za-z]{2,4}[0-9]{2,4}$"


def find_student(students, student_id):
    """Find a student by ID. Return None if the student does not exist."""
    for student in students:
        if student.student_id.upper() == student_id.upper():
            return student
    return None


def ask_text(message):
    """Keep asking until the user types something that is not empty."""
    while True:
        value = input(message).strip()
        if value != "":
            return value
        print("This field cannot be empty. Please try again.")


def ask_student_id(students, check_duplicate=True):
    """Ask for a Student ID and validate its format with a regular expression."""
    while True:
        value = input("Enter Student ID (example: STU001): ").strip()
        if re.match(ID_PATTERN, value) is None:
            print("Invalid ID. Use 2-4 letters followed by 2-4 numbers, e.g. STU001.")
            continue
        if check_duplicate and find_student(students, value) is not None:
            print("That Student ID already exists. Please use another one.")
            continue
        return value.upper()


def ask_date():
    """Ask for a date and make sure it is in YYYY-MM-DD format."""
    while True:
        value = input("Enter Date of Birth (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Invalid date. Please use the format YYYY-MM-DD, e.g. 2008-05-14.")


def ask_gender():
    """Ask for a gender and accept only Male or Female."""
    while True:
        value = input("Enter Gender (Male/Female): ").strip().lower()
        if value == "male" or value == "female":
            return value.capitalize()
        print("Please type Male or Female.")


def ask_score(subject):
    """Ask for a score between 0 and 100."""
    while True:
        value = input("Enter score for " + subject + " (0-100): ").strip()
        try:
            score = int(value)
        except ValueError:
            print("Score must be a whole number.")
            continue
        if score < 0 or score > 100:
            print("Score must be between 0 and 100.")
            continue
        return score


def add_student(students):
    """Collect the details of a new student and add the student to the list."""
    print("\n--- ADD NEW STUDENT ---")
    student_id = ask_student_id(students)
    full_name = ask_text("Enter Full Name: ").title()
    student_class = ask_text("Enter Class/Form (example: SS1A): ").upper()
    gender = ask_gender()
    date_of_birth = ask_date()

    new_student = Student(student_id, full_name, student_class, gender, date_of_birth)
    students.append(new_student)
    save_students(students)
    print("\nStudent " + full_name + " was added successfully.")

    answer = input("Do you want to enter scores now? (y/n): ").strip().lower()
    if answer == "y":
        record_scores(students, new_student)


def search_student(students):
    """Search for a student by ID or by part of the name."""
    print("\n--- SEARCH STUDENT ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    keyword = ask_text("Enter Student ID or part of the name: ").strip().lower()
    found = []
    for student in students:
        if keyword == student.student_id.lower() or keyword in student.full_name.lower():
            found.append(student)

    if len(found) == 0:
        print("No matching student found.")
        return

    print_student_table(found)

    if len(found) == 1:
        answer = input("View this student's report card? (y/n): ").strip().lower()
        if answer == "y":
            position = get_class_position(students, found[0].student_id)
            print_report_card(found[0], position)


def update_student(students):
    """Update the personal information of a student."""
    print("\n--- UPDATE STUDENT INFORMATION ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    student_id = ask_text("Enter Student ID to update: ")
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
        return

    print("Updating: " + student.full_name)
    print("Press Enter to keep the current value.")

    new_name = input("Full Name [" + student.full_name + "]: ").strip()
    if new_name != "":
        student.full_name = new_name.title()

    new_class = input("Class/Form [" + student.student_class + "]: ").strip()
    if new_class != "":
        student.student_class = new_class.upper()

    new_gender = input("Gender [" + student.gender + "]: ").strip()
    if new_gender != "":
        if new_gender.lower() == "male" or new_gender.lower() == "female":
            student.gender = new_gender.capitalize()
        else:
            print("Invalid gender entered, keeping the old value.")

    new_dob = input("Date of Birth [" + student.date_of_birth + "]: ").strip()
    if new_dob != "":
        try:
            datetime.strptime(new_dob, "%Y-%m-%d")
            student.date_of_birth = new_dob
        except ValueError:
            print("Invalid date entered, keeping the old value.")

    save_students(students)
    print("Student information updated.")


def delete_student(students):
    """Delete a student after asking for confirmation."""
    print("\n--- DELETE STUDENT ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    student_id = ask_text("Enter Student ID to delete: ")
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
        return

    answer = input("Are you sure you want to delete " + student.full_name + "? (y/n): ").strip().lower()
    if answer == "y":
        students.remove(student)
        save_students(students)
        print("Student deleted successfully.")
    else:
        print("Delete cancelled.")


def record_scores(students, student=None):
    """Record or update the five subject scores of a student."""
    print("\n--- RECORD / UPDATE SCORES ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    if student is None:
        student_id = ask_text("Enter Student ID: ")
        student = find_student(students, student_id)
        if student is None:
            print("Student not found.")
            return

    print("Recording scores for " + student.full_name + " (" + student.student_id + ")")
    for subject in SUBJECTS:
        student.set_score(subject, ask_score(subject))

    student.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_students(students)

    total = calculate_total(student.scores)
    average = calculate_average(student.scores)
    grade = get_grade(average)
    print("\nScores saved. Total: " + str(total) + ", Average: " + str(average) + ", Grade: " + grade)


def view_report_card(students):
    """Show the report card of one student."""
    print("\n--- VIEW REPORT CARD ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    student_id = ask_text("Enter Student ID: ")
    student = find_student(students, student_id)
    if student is None:
        print("Student not found.")
        return

    if not student.has_scores():
        print("This student has no scores yet. Use option 6 to record scores.")
        return

    position = get_class_position(students, student.student_id)
    print_report_card(student, position)


def view_all_results(students):
    """Show all results, sorted by average or by name."""
    print("\n--- ALL RESULTS ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    choice = input("Sort by (1) Average highest to lowest or (2) Name? Enter 1 or 2: ").strip()

    if choice == "1":
        sorted_students = sort_by_average(students)
        print("\nSorted by average (highest first).")
    elif choice == "2":
        sorted_students = sort_by_name(students)
        print("\nSorted by name.")
    else:
        print("Invalid choice. Showing the normal order.")
        sorted_students = students

    print_student_table(sorted_students)


def save_class_report(students):
    """Save the class report to data/class_report.txt."""
    print("\n--- SAVE TEXT REPORT ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    filename = "data/class_report.txt"
    if save_text_report(students, filename):
        print("Report saved to " + filename)


def export_results_csv(students):
    """Export all results to data/results.csv."""
    print("\n--- EXPORT RESULTS TO CSV ---")
    if len(students) == 0:
        print("No students registered yet.")
        return

    filename = "data/results.csv"
    if export_csv(students, filename):
        print("Results exported to " + filename)


def show_menu():
    """Print the main menu."""
    print("\n" + "=" * 45)
    print(" STUDENT RESULT MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1.  Add new student")
    print("2.  View all students")
    print("3.  Search for a student")
    print("4.  Update student information")
    print("5.  Delete a student")
    print("6.  Record / update scores")
    print("7.  View student report card")
    print("8.  View all results")
    print("9.  Class statistics")
    print("10. Save class report to text file")
    print("11. Export results to CSV")
    print("0.  Exit")
    print("=" * 45)


def main():
    """Start the program, load saved data and show the menu."""
    students = load_students()
    print("Loaded " + str(len(students)) + " student(s) from the data file.")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            print_student_table(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            record_scores(students)
        elif choice == "7":
            view_report_card(students)
        elif choice == "8":
            view_all_results(students)
        elif choice == "9":
            print_statistics(students)
        elif choice == "10":
            save_class_report(students)
        elif choice == "11":
            export_results_csv(students)
        elif choice == "0":
            print("Goodbye! All changes have been saved.")
            break
        else:
            print("Invalid option. Please choose a number from the menu.")


if __name__ == "__main__":
    main()
