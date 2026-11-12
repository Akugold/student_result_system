"""This module contains the Student class."""


class Student:
    """Represents one student in the school."""

    def __init__(self, student_id, full_name, student_class, gender, date_of_birth):
        self.student_id = student_id
        self.full_name = full_name
        self.student_class = student_class
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.scores = {}
        self.result_date = ""

    def set_score(self, subject, score):
        """Save the score of one subject."""
        self.scores[subject] = score

    def get_score(self, subject):
        """Return the score of a subject, or 0 if it was not recorded."""
        return self.scores.get(subject, 0)

    def has_scores(self):
        """Return True if the student has at least one score."""
        return len(self.scores) > 0

    def to_dict(self):
        """Convert the student to a dictionary so it can be saved as JSON."""
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "student_class": self.student_class,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "scores": self.scores,
            "result_date": self.result_date,
        }

    @staticmethod
    def from_dict(data):
        """Create a Student object from a dictionary loaded from JSON."""
        student = Student(
            data["student_id"],
            data["full_name"],
            data["student_class"],
            data["gender"],
            data["date_of_birth"],
        )
        student.scores = data.get("scores", {})
        student.result_date = data.get("result_date", "")
        return student
