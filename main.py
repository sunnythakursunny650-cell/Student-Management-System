import sqlite3
from student import Student
import database

conn = sqlite3.connect("students.db")
cursor = conn.cursor()


def add_student():
    student_id = int(input("Enter Student ID: "))
    name = input("Enter Student Name: ")
    course = input("Enter Course: ")
    marks = float(input("Enter Marks: "))

    student = Student(student_id, name, course, marks)

    cursor.execute("""
    INSERT INTO students(student_id, name, course, marks)
    VALUES (?, ?, ?, ?)
    """, (
        student.student_id,
        student.name,
        student.course,
        student.marks
    ))

    conn.commit()
    print("Student Added Successfully ✅")


def view_students():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No Student Records Found.")
        return

    print("\n========== Student Records ==========")

    for student in students:
        print(f"Student ID   : {student[0]}")
        print(f"Name         : {student[1]}")
        print(f"Course       : {student[2]}")
        print(f"Marks        : {student[3]}")
        print("----------------------------------------")


def update_student():

    student_id = int(input("Enter Student ID: "))
    name = input("Enter New Name: ")
    course = input("Enter New Course: ")
    marks = float(input("Enter New Marks: "))

    cursor.execute("""
    UPDATE students
    SET name = ?, course = ?, marks = ?
    WHERE student_id = ?
    """, (name, course, marks, student_id))

    conn.commit()

    if cursor.rowcount == 0:
        print("Student Not Found.")
    else:
        print("Student Updated Successfully ✅")


def delete_student():

    student_id = int(input("Enter Student ID to Delete: "))

    cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("Student Not Found.")
    else:
        print("Student Deleted Successfully ✅")


while True:

    print("\n========== Student Management System ==========")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        print("Thank you for using Student Management System 😊")
        break

    else:
        print("Invalid Choice! Please try again.")


