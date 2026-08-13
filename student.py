class Student:

    def __init__(
        self,
        student_id,
        name,
        email,
        mobile,
        gender,
        date_of_birth,
        course,
        attendance,
        marks
    ):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.mobile = mobile
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.course = course
        self.attendance = attendance
        self.marks = marks

        # Calculate Grade
        if marks >= 90:
            self.grade = "A+"
        elif marks >= 80:
            self.grade = "A"
        elif marks >= 70:
            self.grade = "B"
        elif marks >= 60:
            self.grade = "C"
        elif marks >= 50:
            self.grade = "D"
        else:
            self.grade = "F"

        # Calculate Status
        if marks >= 40 and attendance >= 75:
            self.status = "Pass"
        else:
            self.status = "Fail"