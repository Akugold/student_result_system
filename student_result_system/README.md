# Student Result Management System

A simple command-line application built with Python for a secondary school. It lets the
school register students, record scores in five subjects, calculate totals, averages and
grades, print report cards, view class statistics and save all data to a JSON file.

This project was written with beginner-friendly Python only (no external libraries).

## Features

### Student Management
- Add a new student (Student ID, Full Name, Class/Form, Gender, Date of Birth)
- View all registered students
- Search for a student by ID or by name
- Update student information
- Delete a student record (with confirmation)

### Score / Result Management
- Record scores for five subjects per student
- Calculate total score and average
- Assign a grade based on the average
- Update existing scores at any time
- Display a full student report card

### Reporting and Analysis
- List all students with totals, averages and grades
- Sort results by average (highest first) or by name
- Show class statistics: highest average, lowest average, class average,
  best student(s) and subject analysis
- Save a text report to `data/class_report.txt`
- Export results to `data/results.csv`

### Data Persistence
- All data is saved to `data/students.json`
- Data is loaded automatically when the program starts
- If the data file does not exist, the program starts with an empty list

## Subjects

The five subjects are defined in `results.py`:

1. English Language
2. Mathematics
3. Basic Science
4. Social Studies
5. Computer Studies

You can change the subject names or add more subjects by editing the `SUBJECTS` list.

## Grading Scale

| Average Score | Grade | Remark     |
|---------------|-------|------------|
| 70 - 100      | A     | Excellent  |
| 60 - 69       | B     | Very Good  |
| 50 - 59       | C     | Good       |
| 40 - 49       | D     | Pass       |
| 0 - 39        | F     | Fail       |

## Project Structure

```
student_result_system/
├── main.py              # Entry point and main menu
├── student.py           # Student class
├── results.py           # Score calculation and grading logic
├── storage.py           # Load and save data (JSON)
├── reports.py           # Report generation and CSV export
├── data/
│   └── students.json    # Saved student data
├── .gitignore
└── README.md
```

## How to Run

1. Install Python 3 (version 3.8 or newer). Check with:

   ```
   python --version
   ```

2. Open a terminal and move into the project folder:

   ```
   cd student_result_system
   ```

3. Run the program:

   ```
   python main.py
   ```

4. Choose an option from the menu by typing its number and pressing Enter.

## How to Use

1. Choose option **1** to add a student.
   - Student ID must be 2-4 letters followed by 2-4 numbers, for example `STU001`.
   - Date of Birth must be in `YYYY-MM-DD` format, for example `2008-05-14`.
2. Choose option **6** to record scores for the five subjects (0-100).
3. Choose option **7** to view a report card.
4. Choose option **8** to view all results sorted by average or name.
5. Choose option **9** to see class statistics.
6. Choose option **10** to save a text report.
7. Choose option **11** to export results to CSV.
8. Choose option **0** to exit. Your data is already saved after every change.

The sample file `data/students.json` contains one example student. Delete the contents
(or delete the file) to start with an empty school.

## Python Concepts Used

- Variables, data types and type conversion (`int()`, `str()`, `round()`)
- Flow control: `if` / `elif` / `else`, `for` loops, `while` loops
- Lists, tuples and dictionaries
- Functions with parameters and return values
- Sorting with `sorted()` and `key`
- Error and exception handling: `try` / `except` / `else` / `finally`
- File handling: reading and writing JSON and CSV files
- Modules: the project is split into several `.py` files
- Object-Oriented Programming: the `Student` class
- Dates and times: `datetime` for date of birth validation and result date
- Standard library: `os`, `json`, `csv`, `re`, `datetime`
- Regular expressions: `re.match()` validates the Student ID format

## Data File Format

`data/students.json` stores a list of students. Each student looks like this:

```json
{
    "student_id": "STU001",
    "full_name": "Godfrey Example",
    "student_class": "SS1A",
    "gender": "Male",
    "date_of_birth": "2008-05-14",
    "scores": {
        "English Language": 72,
        "Mathematics": 85,
        "Basic Science": 68,
        "Social Studies": 74,
        "Computer Studies": 90
    },
    "result_date": "2026-11-11 10:30"
}
```

## Uploading to GitHub

1. Create a GitHub account at https://github.com if you do not have one.
2. Create a new repository named `student_result_system`.
3. Open a terminal inside the project folder and run:

   ```
   git init
   git add .
   git commit -m "Initial commit: student_result_system"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/student-result-system.git
   git push -u origin main
   ```

4. Make more commits as you improve the project, for example:

   ```
   git add .
   git commit -m "student_result_system"
   git push
   ```

## Author

Name: Godfrey Akunna Stephanie
Matric Number: 24/SCI01/089
Course: Python Programming
