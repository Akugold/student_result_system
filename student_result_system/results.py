"""Score calculation and grading logic."""

SUBJECTS = [
    "English Language",
    "Mathematics",
    "Basic Science",
    "Social Studies",
    "Computer Studies",
]


def calculate_total(scores):
    """Add the scores of all subjects together."""
    total = 0
    for subject in SUBJECTS:
        total = total + scores.get(subject, 0)
    return total


def calculate_average(scores):
    """Return the average score of a student."""
    if len(SUBJECTS) == 0:
        return 0
    return round(calculate_total(scores) / len(SUBJECTS), 2)


def get_grade(average):
    """Return the grade that matches an average score."""
    if average >= 70:
        return "A"
    elif average >= 60:
        return "B"
    elif average >= 50:
        return "C"
    elif average >= 40:
        return "D"
    else:
        return "F"


def get_remark(grade):
    """Return a short remark for a grade."""
    remarks = {
        "A": "Excellent",
        "B": "Very Good",
        "C": "Good",
        "D": "Pass",
        "F": "Fail",
    }
    return remarks.get(grade, "No remark")


def sort_by_average(students):
    """Return a new list of students sorted by average, highest first."""
    return sorted(students, key=lambda student: calculate_average(student.scores), reverse=True)


def sort_by_name(students):
    """Return a new list of students sorted by full name."""
    return sorted(students, key=lambda student: student.full_name.lower())


def get_class_position(students, student_id):
    """Return the position of a student when ranked by average score."""
    ranked_students = sort_by_average(students)
    position = 1
    for student in ranked_students:
        if student.student_id == student_id:
            return position
        position = position + 1
    return 0
