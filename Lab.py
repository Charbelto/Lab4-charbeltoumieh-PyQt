import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QScrollArea, QMessageBox, QHBoxLayout, QGridLayout
import json
import re
import csv
from typing import List, Union

class Person:
    """
    This is a base class representation of a person in the School Management System.

    :param name: The name of the person
    :type name: str
    :param age: The age of the person
    :type age: int
    :param email: The email address of the person
    :type email: str
    """

    def __init__(self, name: str, age: int, email: str):

        self.name = name
        self.age = age
        self._email = email

    def introduce(self):
        """
        Prints an introduction of the person.
        """
        print(f"Hi, I'm {self.name}, {self.age} years old.")




class Student(Person):
    """
    This class represents a student in the School Management System. It inherits from the Person class.

    :param name: The name of the student
    :type name: str
    :param age: The age of the student
    :type age: int
    :param email: The email address of the student
    :type email: str
    :param student_id: The unique identifier for the student
    :type student_id: str
    """

    def __init__(self, name: str, age: int, email: str, student_id: str):

        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses: List[Course] = []

    def register_course(self, course: 'Course'):
        """
        Registers the student for a course.

        :param course: The course to register for
        :type course: Course
        """
        self.registered_courses.append(course)
        print(f"{self.name} has registered for {course.course_name}.")


class Instructor(Person):
    """
    This class represents an instructor in the School Management System. It inherits from the Person class.

    :param name: The name of the instructor
    :type name: str
    :param age: The age of the instructor
    :type age: int
    :param email: The email address of the instructor
    :type email: str
    :param instructor_id: The unique identifier for the instructor
    :type instructor_id: str
    """

    def __init__(self, name: str, age: int, email: str, instructor_id: str):

        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses: List['Course'] = []

    def assign_course(self, course: 'Course'):
        """
        Assigns a course to the instructor.

        :param course: The course to assign
        :type course: Course
        """
        self.assigned_courses.append(course)
        print(f"{self.name} is assigned to teach {course.course_name}.")


class Course:
    """
    This class represents a course in the School Management System.

    :param course_id: The unique identifier for the course
    :type course_id: str
    :param course_name: The name of the course
    :type course_name: str
    :param instructor: The instructor teaching the course
    :type instructor: Instructor
    """

    def __init__(self, course_id: str, course_name: str, instructor: Instructor):

        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students: List[Student] = []

    def add_student(self, student: Student):
        """
        Adds a student to the course.

        :param student: The student to add to the course
        :type student: Student
        """
        self.enrolled_students.append(student)
        print(f"{student.name} has been added to {self.course_name}.")


def create_tables():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS instructors (
        instructor_id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        email TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
        course_id TEXT PRIMARY KEY,
        course_name TEXT,
        instructor_id TEXT,
        FOREIGN KEY (instructor_id) REFERENCES instructors (instructor_id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
        student_id TEXT,
        course_id TEXT,
        FOREIGN KEY (student_id) REFERENCES students (student_id),
        FOREIGN KEY (course_id) REFERENCES courses (course_id),
        PRIMARY KEY (student_id, course_id)
    )''')

    conn.commit()
    conn.close()

def save_data_to_file(data: List[Union[Student, Instructor, Course]], filename: str):
    """
    Saves data to a JSON file.

    :param data: The list of objects to save
    :type data: List[Union[Student, Instructor, Course]]
    :param filename: The name of the file to save the data to
    :type filename: str
    """
    with open(filename, 'w') as f:
        json.dump([obj.__dict__ for obj in data], f)


def load_data_from_file(filename: str, class_type: type) -> List[Union[Student, Instructor, Course]]:
    """
    Loads data from a JSON file.

    :param filename: The name of the file to load the data from
    :type filename: str
    :param class_type: The type of class to instantiate (Student, Instructor, or Course)
    :type class_type: type
    :return: A list of instantiated objects
    :rtype: List[Union[Student, Instructor, Course]]
    """
    with open(filename, 'r') as f:
        data = json.load(f)
    return [class_type(**item) for item in data]


def is_valid_email(email: str) -> bool:
    """
    Checks if an email address is valid.

    :param email: The email address to validate
    :type email: str
    :return: True if the email is valid, False otherwise
    :rtype: bool
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_person_data(name: str, age: int, email: str):
    """
    Validates the data for a person (Student or Instructor).

    :param name: The name to validate
    :type name: str
    :param age: The age to validate
    :type age: int
    :param email: The email address to validate
    :type email: str
    :raises ValueError: If any of the data is invalid
    """
    if not name:
        raise ValueError("Name cannot be empty")
    if age < 0:
        raise ValueError("Age cannot be negative")
    if not is_valid_email(email):
        raise ValueError("Invalid email format")


class SchoolManagementSystem(QMainWindow):
    """
    This is the main application window for the School Management System. It handles the user interface and database operations for managing students, instructors, courses, and registrations.
    Attributes:
        layout (QVBoxLayout): The main layout of the application window
        instructor_combo_options (list): A list of instructor options for combo boxes
        table (QTableWidget): The table widget for displaying records
        student_id_input (QLineEdit): Input field for student ID
        student_name_input (QLineEdit): Input field for student name
        student_age_input (QLineEdit): Input field for student age
        student_email_input (QLineEdit): Input field for student email
        instructor_id_input (QLineEdit): Input field for instructor ID
        instructor_name_input (QLineEdit): Input field for instructor name
        instructor_age_input (QLineEdit): Input field for instructor age
        instructor_email_input (QLineEdit): Input field for instructor email
        course_id_input (QLineEdit): Input field for course ID
        course_name_input (QLineEdit): Input field for course name
        course_instructor_combo (QComboBox): Combo box for selecting course instructor
        student_combo (QComboBox): Combo box for selecting a student
        course_combo (QComboBox): Combo box for selecting a course
        search_input (QLineEdit): Input field for search queries
    """
    def __init__(self):
        """
        Constructor method. Initializes the SchoolManagementSystem window.
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 1000, 800)

        central_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        self.layout = QVBoxLayout(central_widget)

        self.instructor_combo_options = []
        self.table = None

        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the application.
        """
        # Student section
        student_layout = QGridLayout()
        self.layout.addWidget(QLabel("Student Management"))
        self.layout.addLayout(student_layout)

        self.student_id_input = QLineEdit()
        self.student_name_input = QLineEdit()
        self.student_age_input = QLineEdit()
        self.student_email_input = QLineEdit()
        
        student_layout.addWidget(QLabel("Student ID:"), 0, 0)
        student_layout.addWidget(self.student_id_input, 0, 1)
        student_layout.addWidget(QLabel("Name:"), 1, 0)
        student_layout.addWidget(self.student_name_input, 1, 1)
        student_layout.addWidget(QLabel("Age:"), 2, 0)
        student_layout.addWidget(self.student_age_input, 2, 1)
        student_layout.addWidget(QLabel("Email:"), 3, 0)
        student_layout.addWidget(self.student_email_input, 3, 1)

        student_button_layout = QHBoxLayout()
        self.add_student_button = QPushButton("Add Student")
        self.add_student_button.clicked.connect(self.add_student)
        self.update_student_button = QPushButton("Update Student")
        self.update_student_button.clicked.connect(self.update_student)
        self.delete_student_button = QPushButton("Delete Student")
        self.delete_student_button.clicked.connect(self.delete_student)
        student_button_layout.addWidget(self.add_student_button)
        student_button_layout.addWidget(self.update_student_button)
        student_button_layout.addWidget(self.delete_student_button)
        student_layout.addLayout(student_button_layout, 4, 0, 1, 2)

        # Instructor section
        instructor_layout = QGridLayout()
        self.layout.addWidget(QLabel("Instructor Management"))
        self.layout.addLayout(instructor_layout)

        self.instructor_id_input = QLineEdit()
        self.instructor_name_input = QLineEdit()
        self.instructor_age_input = QLineEdit()
        self.instructor_email_input = QLineEdit()
        
        instructor_layout.addWidget(QLabel("Instructor ID:"), 0, 0)
        instructor_layout.addWidget(self.instructor_id_input, 0, 1)
        instructor_layout.addWidget(QLabel("Name:"), 1, 0)
        instructor_layout.addWidget(self.instructor_name_input, 1, 1)
        instructor_layout.addWidget(QLabel("Age:"), 2, 0)
        instructor_layout.addWidget(self.instructor_age_input, 2, 1)
        instructor_layout.addWidget(QLabel("Email:"), 3, 0)
        instructor_layout.addWidget(self.instructor_email_input, 3, 1)

        instructor_button_layout = QHBoxLayout()
        self.add_instructor_button = QPushButton("Add Instructor")
        self.add_instructor_button.clicked.connect(self.add_instructor)
        self.update_instructor_button = QPushButton("Update Instructor")
        self.update_instructor_button.clicked.connect(self.update_instructor)
        self.delete_instructor_button = QPushButton("Delete Instructor")
        self.delete_instructor_button.clicked.connect(self.delete_instructor)
        instructor_button_layout.addWidget(self.add_instructor_button)
        instructor_button_layout.addWidget(self.update_instructor_button)
        instructor_button_layout.addWidget(self.delete_instructor_button)
        instructor_layout.addLayout(instructor_button_layout, 4, 0, 1, 2)

        # Course section
        course_layout = QGridLayout()
        self.layout.addWidget(QLabel("Course Management"))
        self.layout.addLayout(course_layout)

        self.course_id_input = QLineEdit()
        self.course_name_input = QLineEdit()
        self.course_instructor_combo = QComboBox()
        
        course_layout.addWidget(QLabel("Course ID:"), 0, 0)
        course_layout.addWidget(self.course_id_input, 0, 1)
        course_layout.addWidget(QLabel("Course Name:"), 1, 0)
        course_layout.addWidget(self.course_name_input, 1, 1)
        course_layout.addWidget(QLabel("Instructor:"), 2, 0)
        course_layout.addWidget(self.course_instructor_combo, 2, 1)

        course_button_layout = QHBoxLayout()
        self.add_course_button = QPushButton("Add Course")
        self.add_course_button.clicked.connect(self.add_course)
        self.update_course_button = QPushButton("Update Course")
        self.update_course_button.clicked.connect(self.update_course)
        self.delete_course_button = QPushButton("Delete Course")
        self.delete_course_button.clicked.connect(self.delete_course)
        course_button_layout.addWidget(self.add_course_button)
        course_button_layout.addWidget(self.update_course_button)
        course_button_layout.addWidget(self.delete_course_button)
        course_layout.addLayout(course_button_layout, 3, 0, 1, 2)

        # Registration section
        registration_layout = QGridLayout()
        self.layout.addWidget(QLabel("Course Registration"))
        self.layout.addLayout(registration_layout)

        self.student_combo = QComboBox()
        self.course_combo = QComboBox()
        
        registration_layout.addWidget(QLabel("Student:"), 0, 0)
        registration_layout.addWidget(self.student_combo, 0, 1)
        registration_layout.addWidget(QLabel("Course:"), 1, 0)
        registration_layout.addWidget(self.course_combo, 1, 1)

        self.register_button = QPushButton("Register Student to Course")
        self.register_button.clicked.connect(self.register_student_to_course)
        registration_layout.addWidget(self.register_button, 2, 0, 1, 2)

        # Other buttons
        self.display_records_button = QPushButton("Display Records")
        self.display_records_button.clicked.connect(self.display_records)
        self.layout.addWidget(self.display_records_button)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_records)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        self.layout.addLayout(search_layout)

        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_data)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_button)

        self.update_dropdowns()

    def update_dropdowns(self):
        """Updates the combo boxes with the latest data from the database."""
        self.course_instructor_combo.clear()
        self.student_combo.clear()
        self.course_combo.clear()

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT instructor_id, name FROM instructors")
        instructors = cursor.fetchall()
        self.course_instructor_combo.addItems([f"{i[0]} - {i[1]}" for i in instructors])

        cursor.execute("SELECT student_id, name FROM students")
        students = cursor.fetchall()
        self.student_combo.addItems([f"{s[0]} - {s[1]}" for s in students])

        cursor.execute("SELECT course_id, course_name FROM courses")
        courses = cursor.fetchall()
        self.course_combo.addItems([f"{c[0]} - {c[1]}" for c in courses])

        conn.close()

    def show_popup(self, message, is_error=False):
        """
        Displays a popup message to the user.
        
        :param message: The message to display
        :type message: str
        :param is_error: Whether the message is an error message, defaults to False
        :type is_error: bool, optional

        """
        msg_box = QMessageBox()
        msg_box.setText(message)
        if is_error:
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Error")
        else:
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Success")
        msg_box.exec_()

    def add_student(self):
        """Adds a student to the database."""
        try:
            student_id = self.student_id_input.text()
            name = self.student_name_input.text()
            age = int(self.student_age_input.text())
            email = self.student_email_input.text()

            validate_person_data(name, age, email)

            student = Student(name, age, email, student_id)
            self.add_to_database('students', student)
            self.show_popup(f"Student {name} added successfully.")
            self.update_dropdowns()
        except ValueError as e:
            self.show_popup(f"Error adding student: {str(e)}", is_error=True)

    def update_student(self):
        """Updates a student in the database."""
        try:
            student_id = self.student_id_input.text()
            name = self.student_name_input.text()
            age = int(self.student_age_input.text())
            email = self.student_email_input.text()

            validate_person_data(name, age, email)

            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET name=?, age=?, email=? WHERE student_id=?",
                           (name, age, email, student_id))
            conn.commit()
            conn.close()

            self.show_popup(f"Student {name} updated successfully.")
            self.update_dropdowns()
        except ValueError as e:
            self.show_popup(f"Error updating student: {str(e)}", is_error=True)

    def delete_student(self):
        """Deletes a student from the database."""
        student_id = self.student_id_input.text()
        if not student_id:
            self.show_popup("Please enter a student ID to delete.", is_error=True)
            return

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        # Delete student's registrations first
        cursor.execute("DELETE FROM registrations WHERE student_id=?", (student_id,))

        # Then delete the student
        cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        
        if cursor.rowcount == 0:
            self.show_popup(f"No student found with ID {student_id}", is_error=True)
        else:
            conn.commit()
            self.show_popup(f"Student with ID {student_id} deleted successfully.")
            self.update_dropdowns()

        conn.close()

    def add_instructor(self):
        """Adds an instructor to the database."""
        try:
            instructor_id = self.instructor_id_input.text()
            name = self.instructor_name_input.text()
            age = int(self.instructor_age_input.text())
            email = self.instructor_email_input.text()

            validate_person_data(name, age, email)

            instructor = Instructor(name, age, email, instructor_id)
            self.add_to_database('instructors', instructor)
            self.show_popup(f"Instructor {name} added successfully.")
            self.update_dropdowns()
        except ValueError as e:
            self.show_popup(f"Error adding instructor: {str(e)}", is_error=True)

    def update_instructor(self):
        """Updates an instructor in the database."""
        try:
            instructor_id = self.instructor_id_input.text()
            name = self.instructor_name_input.text()
            age = int(self.instructor_age_input.text())
            email = self.instructor_email_input.text()

            validate_person_data(name, age, email)

            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE instructors SET name=?, age=?, email=? WHERE instructor_id=?",
                           (name, age, email, instructor_id))
            conn.commit()
            conn.close()

            self.show_popup(f"Instructor {name} updated successfully.")
            self.update_dropdowns()
        except ValueError as e:
            self.show_popup(f"Error updating instructor: {str(e)}", is_error=True)

    def delete_instructor(self):
        """Deletes an instructor from the database."""
        instructor_id = self.instructor_id_input.text()
        if not instructor_id:
            self.show_popup("Please enter an instructor ID to delete.", is_error=True)
            return

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        # Check if instructor is assigned to any courses
        cursor.execute("SELECT COUNT(*) FROM courses WHERE instructor_id=?", (instructor_id,))
        course_count = cursor.fetchone()[0]

        if course_count > 0:
            self.show_popup(f"Cannot delete instructor. They are assigned to {course_count} course(s).", is_error=True)
        else:
            # Delete the instructor
            cursor.execute("DELETE FROM instructors WHERE instructor_id=?", (instructor_id,))
            
            if cursor.rowcount == 0:
                self.show_popup(f"No instructor found with ID {instructor_id}", is_error=True)
            else:
                conn.commit()
                self.show_popup(f"Instructor with ID {instructor_id} deleted successfully.")
                self.update_dropdowns()

        conn.close()

    def add_course(self):
        """Adds a course to the database."""
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()
        instructor_id = self.course_instructor_combo.currentText().split(' - ')[0]

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (course_id, course_name, instructor_id) VALUES (?, ?, ?)",
                       (course_id, course_name, instructor_id))
        conn.commit()
        conn.close()

        self.show_popup(f"Course {course_name} added successfully.")
        self.update_dropdowns()

    def update_course(self):
        """Updates a course in the database."""
        course_id = self.course_id_input.text()
        course_name = self.course_name_input.text()
        instructor_id = self.course_instructor_combo.currentText().split(' - ')[0]

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE courses SET course_name=?, instructor_id=? WHERE course_id=?",
                       (course_name, instructor_id, course_id))
        
        if cursor.rowcount == 0:
            self.show_popup(f"No course found with ID {course_id}", is_error=True)
        else:
            conn.commit()
            self.show_popup(f"Course {course_name} updated successfully.")
            self.update_dropdowns()

        conn.close()

    def delete_course(self):
        """Deletes a course from the database."""
        course_id = self.course_id_input.text()
        if not course_id:
            self.show_popup("Please enter a course ID to delete.", is_error=True)
            return

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        # Delete course registrations first
        cursor.execute("DELETE FROM registrations WHERE course_id=?", (course_id,))

        # Then delete the course
        cursor.execute("DELETE FROM courses WHERE course_id=?", (course_id,))
        
        if cursor.rowcount == 0:
            self.show_popup(f"No course found with ID {course_id}", is_error=True)
        else:
            conn.commit()
            self.show_popup(f"Course with ID {course_id} deleted successfully.")
            self.update_dropdowns()

        conn.close()

    def register_student_to_course(self):
        """Registers a student to a course."""
        student_id = self.student_combo.currentText().split(' - ')[0]
        course_id = self.course_combo.currentText().split(' - ')[0]

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO registrations (student_id, course_id) VALUES (?, ?)",
                           (student_id, course_id))
            conn.commit()
            self.show_popup(f"Student {student_id} registered to course {course_id} successfully.")
        except sqlite3.IntegrityError:
            self.show_popup(f"Student {student_id} is already registered to course {course_id}.", is_error=True)
        finally:
            conn.close()

    def add_to_database(self, table: str, obj: Union[Student, Instructor]):
        """Adds a new record to the specified table in the database.

:param table: The name of the table to add the record to
:type table: str
:param obj: The object (Student or Instructor) to add to the database
:type obj: Union[Student, Instructor]"""
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        if table == 'students':
            cursor.execute("INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)",
                           (obj.student_id, obj.name, obj.age, obj._email))
        elif table == 'instructors':
            cursor.execute("INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)",
                           (obj.instructor_id, obj.name, obj.age, obj._email))

        conn.commit()
        conn.close()

    def display_records(self):
        """Displays all records in the database."""
        if self.table:
            self.layout.removeWidget(self.table)
            self.table.deleteLater()
            self.table = None

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Type", "ID", "Name", "Age/Course Name", "Email/Instructor ID"])

        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT 'Student' as type, student_id, name, age, email FROM students")
        students = cursor.fetchall()

        cursor.execute("SELECT 'Instructor' as type, instructor_id, name, age, email FROM instructors")
        instructors = cursor.fetchall()

        cursor.execute("SELECT 'Course' as type, course_id, course_name, instructor_id, '' FROM courses")
        courses = cursor.fetchall()

        conn.close()

        all_records = students + instructors + courses
        self.table.setRowCount(len(all_records))

        for row, record in enumerate(all_records):
            for col, value in enumerate(record):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.layout.addWidget(self.table)

    def search_records(self):
        """Searches for records in the database based on the search query."""
        if self.table:
            self.layout.removeWidget(self.table)
            self.table.deleteLater()
            self.table = None

        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Type", "ID", "Name", "Age/Course Name", "Email/Instructor ID"])

        query = self.search_input.text()
        conn = sqlite3.connect('school_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT 'Student' as type, student_id, name, age, email FROM students WHERE name LIKE ? OR student_id LIKE ?",
                       (f"%{query}%", f"%{query}%"))
        students = cursor.fetchall()

        cursor.execute("SELECT 'Instructor' as type, instructor_id, name, age, email FROM instructors WHERE name LIKE ? OR instructor_id LIKE ?",
                       (f"%{query}%", f"%{query}%"))
        instructors = cursor.fetchall()

        cursor.execute("SELECT 'Course' as type, course_id, course_name, instructor_id, '' FROM courses WHERE course_name LIKE ? OR course_id LIKE ?",
                       (f"%{query}%", f"%{query}%"))
        courses = cursor.fetchall()

        conn.close()

        all_records = students + instructors + courses
        self.table.setRowCount(len(all_records))

        for row, record in enumerate(all_records):
            for col, value in enumerate(record):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        self.layout.addWidget(self.table)

    def save_data(self):
        """Saves the data from the database to JSON files."""
        try:
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM students")
            students = [Student(name=row[1], age=row[2], email=row[3], student_id=row[0]) for row in cursor.fetchall()]

            cursor.execute("SELECT * FROM instructors")
            instructors = [Instructor(name=row[1], age=row[2], email=row[3], instructor_id=row[0]) for row in cursor.fetchall()]

            cursor.execute("SELECT * FROM courses")
            courses = []
            for row in cursor.fetchall():
                instructor = next((i for i in instructors if i.instructor_id == row[2]), None)
                courses.append(Course(course_id=row[0], course_name=row[1], instructor=instructor))

            conn.close()

            save_data_to_file(students, 'students.json')
            save_data_to_file(instructors, 'instructors.json')
            save_data_to_file(courses, 'courses.json')

            self.show_popup("Data saved successfully.")
        except Exception as e:
            self.show_popup(f"Error saving data: {str(e)}", is_error=True)

    def load_data(self):
        """Loads the data from JSON files into the database."""
        try:
            students = load_data_from_file('students.json', Student)
            instructors = load_data_from_file('instructors.json', Instructor)
            courses = load_data_from_file('courses.json', Course)

            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            cursor.execute("DELETE FROM registrations")
            cursor.execute("DELETE FROM courses")
            cursor.execute("DELETE FROM students")
            cursor.execute("DELETE FROM instructors")

            for student in students:
                cursor.execute("INSERT INTO students (student_id, name, age, email) VALUES (?, ?, ?, ?)",
                               (student.student_id, student.name, student.age, student._email))

            for instructor in instructors:
                cursor.execute("INSERT INTO instructors (instructor_id, name, age, email) VALUES (?, ?, ?, ?)",
                               (instructor.instructor_id, instructor.name, instructor.age, instructor._email))

            for course in courses:
                instructor_id = next((i.instructor_id for i in instructors if i.name == course.instructor.name), None)
                cursor.execute("INSERT INTO courses (course_id, course_name, instructor_id) VALUES (?, ?, ?)",
                               (course.course_id, course.course_name, instructor_id))

            conn.commit()
            conn.close()

            self.show_popup("Data loaded successfully.")
            self.update_dropdowns()
        except Exception as e:
            self.show_popup(f"Error loading data: {str(e)}", is_error=True)

    def export_to_csv(self):
        """Exports the data from the database to a CSV file."""
        try:
            conn = sqlite3.connect('school_management.db')
            cursor = conn.cursor()

            cursor.execute("SELECT 'Student' as type, student_id, name, age, email FROM students")
            students = cursor.fetchall()

            cursor.execute("SELECT 'Instructor' as type, instructor_id, name, age, email FROM instructors")
            instructors = cursor.fetchall()

            cursor.execute("SELECT 'Course' as type, course_id, course_name, instructor_id, '' FROM courses")
            courses = cursor.fetchall()

            cursor.execute("SELECT 'Registration' as type, student_id, course_id, '', '' FROM registrations")
            registrations = cursor.fetchall()

            conn.close()

            with open('school_data.csv', 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Type', 'ID', 'Name', 'Age/Course Name', 'Email/Instructor ID'])

                for record in students + instructors + courses + registrations:
                    csvwriter.writerow(record)

            self.show_popup("Data exported to CSV successfully.")
        except Exception as e:
            self.show_popup(f"Error exporting data: {str(e)}", is_error=True)

def main():
    """The main function that runs the School Management System application."""
    create_tables()
    app = QApplication([])
    window = SchoolManagementSystem()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()