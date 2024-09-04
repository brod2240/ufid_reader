import sqlite3

# Function to create tables if they don't exist
def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        student_id_number TEXT PRIMARY KEY,
                        iso TEXT UNIQUE,
                        first_name TEXT,
                        last_name TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                        course_number TEXT PRIMARY KEY
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS classes (
                        class_number INTEGER PRIMARY KEY,
                        course_number TEXT,
                        FOREIGN KEY (course_number) REFERENCES courses(course_number)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS class_students (
                        class_number INTEGER,
                        student_id_number TEXT,
                        FOREIGN KEY (class_number) REFERENCES classes(class_number),
                        FOREIGN KEY (student_id_number) REFERENCES students(student_id_number),
                        UNIQUE(class_number, student_id_number)
                    )''')


# Function to add a student to the students table
def add_student(cursor, iso, student_id_number, first_name, last_name):
    # Check if the student already exists
    cursor.execute('''SELECT student_id_number FROM students WHERE student_id_number = ?''', (student_id_number,))
    existing_student = cursor.fetchone()
    if existing_student:
        print("Student already exists.")
        return
    else:
        cursor.execute('''INSERT INTO students (iso, student_id_number, first_name, last_name) 
                          VALUES (?, ?, ?, ?)''', (iso, student_id_number, first_name, last_name))
        print("Student added successfully.")

# Function to add a course to the courses table
def add_course(cursor, course_number):
    # Check if the course number already exists
    cursor.execute('''SELECT course_number FROM courses WHERE course_number = ?''', (course_number,))
    existing_course = cursor.fetchone()
    if existing_course:
        print("Course already exists.")
        return
    else:
        cursor.execute('''INSERT INTO courses (course_number) VALUES (?)''', (course_number,))
        print("Course added successfully.")

# Function to add a class to the classes table
def add_class(cursor, class_number, course_number):
    # Check if the class already exists
    cursor.execute('''SELECT class_number FROM classes WHERE class_number = ? AND course_number = ?''', (class_number, course_number))
    existing_class = cursor.fetchone()
    if existing_class:
        print("Class already exists.")
        return
    else:
        cursor.execute('''INSERT INTO classes (class_number, course_number) VALUES (?, ?)''', (class_number, course_number))
        print("Class added successfully.")

# Function to enroll a student in a class using student ID number and class number
def enroll_student_in_class(cursor, student_id_number, class_number):
    # Query student_id based on student_id_number
    cursor.execute('''SELECT student_id_number FROM students WHERE student_id_number = ?''', (student_id_number,))
    student_result = cursor.fetchone()
    if not student_result:
        print(f"Student with ID number {student_id_number} not found.")
        return

    student_id_number = student_result[0]

    # Query class_id based on class_number
    cursor.execute('''SELECT class_number FROM classes WHERE class_number = ?''', (class_number,))
    class_result = cursor.fetchone()
    if not class_result:
        print(f"Class with number {class_number} not found.")
        return

    class_number = class_result[0]

    # Enroll student in class
    try:
        cursor.execute('''INSERT INTO class_students (class_number, student_id_number) VALUES (?, ?)''', (class_number, student_id_number))
        print("Student enrolled successfully.")
    except sqlite3.IntegrityError:
        print("Student is already enrolled in this class.")



# Connect to the SQLite database
conn = sqlite3.connect('StudentCourse.db')
cursor = conn.cursor()

# Create tables if they don't exist
create_tables(cursor)

# Example usage: Add students
add_student(cursor, '6008600002030530', '15854874', 'Aaron', 'Song')
add_student(cursor, '6008600002046233', '93549135', 'John', 'Fang-Wu')

# Example usage: Add courses
add_course(cursor, 'CEN3907C')
add_course(cursor, 'EEL4712C')
add_course(cursor, 'EEL3135')
add_course(cursor, 'CAP3034')
add_course(cursor, 'CAP3020')
add_course(cursor, 'COP4600')
add_course(cursor, 'EEL3872')
add_course(cursor, 'EGS4034')

# Example usage: Add classes with course_number
add_class(cursor, 27483, 'CEN3907C')  

add_class(cursor, 11410, 'EEL4712C') 
add_class(cursor, 11411, 'EEL4712C')  
add_class(cursor, 11412, 'EEL4712C')  
add_class(cursor, 11426, 'EEL4712C')  
add_class(cursor, 11427, 'EEL4712C')  
add_class(cursor, 11428, 'EEL4712C')  
add_class(cursor, 11429, 'EEL4712C') 
add_class(cursor, 11430, 'EEL4712C')  
add_class(cursor, 11431, 'EEL4712C') 
add_class(cursor, 11432, 'EEL4712C')  
add_class(cursor, 11433, 'EEL4712C') 
add_class(cursor, 11453, 'EEL4712C')  
add_class(cursor, 11454, 'EEL4712C') 
add_class(cursor, 11455, 'EEL4712C')  
add_class(cursor, 29093, 'EEL4712C')

add_class(cursor, 11563, 'EEL3135')
add_class(cursor, 11564, 'EEL3135')

add_class(cursor, 11214, 'EEL3135')

add_class(cursor, 11197, 'CAP3020')

add_class(cursor, 10808, 'COP4600')
add_class(cursor, 10809, 'COP4600')
add_class(cursor, 10810, 'COP4600')
add_class(cursor, 10811, 'COP4600')
add_class(cursor, 10812, 'COP4600')
add_class(cursor, 10814, 'COP4600')
add_class(cursor, 26083, 'COP4600')
add_class(cursor, 30754, 'COP4600')
add_class(cursor, 30755, 'COP4600')
add_class(cursor, 30883, 'COP4600')
add_class(cursor, 30884, 'COP4600')

add_class(cursor, 23607, 'EEL3872')
add_class(cursor, 24397, 'EEL3872')

add_class(cursor, 12692, 'EGS4034')
add_class(cursor, 12693, 'EGS4034')
add_class(cursor, 12694, 'EGS4034')
add_class(cursor, 12695, 'EGS4034')
add_class(cursor, 22849, 'EGS4034')
add_class(cursor, 26566, 'EGS4034')
add_class(cursor, 29448, 'EGS4034')


# Example usage: Enroll students in classes using student ID number and class number
enroll_student_in_class(cursor, '15854874', 27483)
enroll_student_in_class(cursor, '15854874', 11427)
enroll_student_in_class(cursor, '15854874', 11563)
enroll_student_in_class(cursor, '15854874', 11214)

enroll_student_in_class(cursor, '93549135', 27483)
enroll_student_in_class(cursor, '93549135', 11197)
enroll_student_in_class(cursor, '93549135', 26083)
enroll_student_in_class(cursor, '93549135', 24397)
enroll_student_in_class(cursor, '93549135', 12693)

# Commit the changes and close the connection
conn.commit()
conn.close()