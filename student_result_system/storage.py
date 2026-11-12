"""Functions for loading and saving data with JSON."""

import json
import os

from student import Student

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "students.json")


def load_students():
    """Load students from the JSON file. Return an empty list if it is missing."""
    if not os.path.exists(DATA_FILE):
        print("No data file found. A new one will be created when you add a student.")
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: the data file is damaged or unreadable. Starting with no students.")
        return []

    students = []
    for item in data:
        students.append(Student.from_dict(item))
    return students


def save_students(students):
    """Save the list of students to the JSON file."""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    data = []
    for student in students:
        data.append(student.to_dict())

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        return True
    except OSError:
        print("Error: the data could not be saved.")
        return False
