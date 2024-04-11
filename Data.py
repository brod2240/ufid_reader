import sqlite3

# Function to create tables if they don't exist
def create_tables(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                    UFID TEXT,
                    ISO TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    class_number1 TEXT,
                    class_number2 TEXT,
                    class_number3 TEXT,
                    class_number4 TEXT,
                    class_number5 TEXT,
                    class_number6 TEXT,
                    class_number7 TEXT,
                    class_number8 TEXT,
                    PRIMARY KEY (UFID, ISO)
                )''')

def add_student(UFID, ISO, first_name, last_name, *class_numbers):
    # Check if the student already exists
    cursor.execute("SELECT * FROM student WHERE UFID = ? AND ISO = ?", (UFID, ISO))
    existing_student = cursor.fetchone()

    # If the student already exists, print a message and return
    if existing_student:
        print("Student with UFID {} and ISO {} already exists.".format(UFID, ISO))
        return
    else:
        # Insert data into the student table
        cursor.execute("INSERT INTO student (UFID, ISO, first_name, last_name, class_number1, class_number2, class_number3, class_number4, class_number5, class_number6, class_number7, class_number8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (UFID, ISO, first_name, last_name, *class_numbers))
        print("Student added successfully.")

# Connect to the SQLite database
conn = sqlite3.connect('StudentCourse2.db')
cursor = conn.cursor()

# Create tables if they don't exist
create_tables(cursor)

add_student("15854874", "6008600002030530", "Aaron", "Song", "27483", "11427", "11563", "11214", None, None, None, None)
add_student("93549135", "6008600002046233", "John", "Fang-Wu", "27483", "11197", "26083", "24397", "12693", None, None, None)

# Commit the changes and close the connection
conn.commit()
conn.close()