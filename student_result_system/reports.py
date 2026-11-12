"""Functions for displaying and saving reports."""

import csv
import os
from datetime import datetime

from results import (
    SUBJECTS,
    calculate_total,
    calculate_average,
    get_grade,
    get_remark,
)


def print_student_table(students):
    """Print a simple table of students with their results."""
    if len(students) == 0:
        print("\nNo students to display.")
        return

    print("\n" + "-" * 78)
    print(f"{'ID':<10}{'Name':<28}{'Class':<10}{'Total':<8}{'Average':<9}{'Grade':<6}")
    print("-" * 78)
    for student in students:
        total = calculate_total(student.scores)
        average = calculate_average(student.scores)
        grade = get_grade(average)
        name = student.full_name[:26]
        print(f"{student.student_id:<10}{name:<28}{student.student_class:<10}{total:<8}{average:<9}{grade:<6}")
    print("-" * 78)
    print("Total students: " + str(len(students)))


def print_report_card(student, position=0):
    """Print the full report card of one student."""
    total = calculate_total(student.scores)
    average = calculate_average(student.scores)
    grade = get_grade(average)
    remark = get_remark(grade)

    print("\n" + "=" * 45)
    print(" " * 10 + "STUDENT REPORT CARD")
    print("=" * 45)
    print("Student ID    : " + student.student_id)
    print("Full Name     : " + student.full_name)
    print("Class/Form    : " + student.student_class)
    print("Gender        : " + student.gender)
    print("Date of Birth : " + student.date_of_birth)
    if student.result_date != "":
        print("Result Date   : " + student.result_date)
    print("-" * 45)
    print(f"{'Subject':<25}{'Score':>10}")
    print("-" * 45)
    for subject in SUBJECTS:
        score = student.get_score(subject)
        print(f"{subject:<25}{score:>10}")
    print("-" * 45)
    print("Total Score   : " + str(total))
    print("Average       : " + str(average))
    print("Grade         : " + grade)
    print("Remark        : " + remark)
    if position > 0:
        print("Position      : " + str(position))
    print("=" * 45)


def print_statistics(students):
    """Print the highest, lowest and average score of the class."""
    if len(students) == 0:
        print("\nNo students to analyse.")
        return

    averages = []
    for student in students:
        averages.append(calculate_average(student.scores))

    highest = max(averages)
    lowest = min(averages)
    class_average = round(sum(averages) / len(averages), 2)

    best_students = []
    for student in students:
        if calculate_average(student.scores) == highest:
            best_students.append(student.full_name)

    print("\n" + "=" * 45)
    print(" " * 12 + "CLASS STATISTICS")
    print("=" * 45)
    print("Number of students : " + str(len(students)))
    print("Highest average    : " + str(highest))
    print("Lowest average     : " + str(lowest))
    print("Class average      : " + str(class_average))
    print("Best student(s)    : " + ", ".join(best_students))
    print("=" * 45)

    print("\nSubject analysis:")
    print(f"{'Subject':<25}{'Class Average':>15}")
    print("-" * 40)
    for subject in SUBJECTS:
        total = 0
        for student in students:
            total = total + student.get_score(subject)
        subject_average = round(total / len(students), 2)
        print(f"{subject:<25}{subject_average:>15}")


def build_text_report(students):
    """Build the text of the class report and return it as one string."""
    lines = []
    lines.append("STUDENT RESULT MANAGEMENT SYSTEM")
    lines.append("Class Report")
    lines.append("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("=" * 70)
    lines.append(f"{'ID':<10}{'Name':<26}{'Class':<8}{'Total':<8}{'Average':<9}{'Grade':<6}")
    lines.append("-" * 70)

    for student in students:
        total = calculate_total(student.scores)
        average = calculate_average(student.scores)
        grade = get_grade(average)
        name = student.full_name[:24]
        lines.append(f"{student.student_id:<10}{name:<26}{student.student_class:<8}{total:<8}{average:<9}{grade:<6}")

    lines.append("-" * 70)
    lines.append("Total students: " + str(len(students)))

    if len(students) > 0:
        averages = []
        for student in students:
            averages.append(calculate_average(student.scores))
        lines.append("Highest average: " + str(max(averages)))
        lines.append("Lowest average : " + str(min(averages)))
        lines.append("Class average  : " + str(round(sum(averages) / len(averages), 2)))

    return "\n".join(lines)


def save_text_report(students, filename):
    """Save the class report to a text file."""
    folder = os.path.dirname(filename)
    if folder != "" and not os.path.exists(folder):
        os.makedirs(folder)

    report_text = build_text_report(students)

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report_text)
        return True
    except OSError:
        print("Error: the report could not be saved.")
        return False


def export_csv(students, filename):
    """Export all results to a CSV file."""
    folder = os.path.dirname(filename)
    if folder != "" and not os.path.exists(folder):
        os.makedirs(folder)

    header = ["Student ID", "Full Name", "Class", "Gender", "Date of Birth"]
    for subject in SUBJECTS:
        header.append(subject)
    header.append("Total")
    header.append("Average")
    header.append("Grade")

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)

            for student in students:
                row = [
                    student.student_id,
                    student.full_name,
                    student.student_class,
                    student.gender,
                    student.date_of_birth,
                ]
                for subject in SUBJECTS:
                    row.append(student.get_score(subject))
                row.append(calculate_total(student.scores))
                row.append(calculate_average(student.scores))
                row.append(get_grade(calculate_average(student.scores)))
                writer.writerow(row)
        return True
    except OSError:
        print("Error: the CSV file could not be saved.")
        return False
