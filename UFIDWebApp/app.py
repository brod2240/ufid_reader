# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from api.courseFetch import fetch_courses
import sqlite3
import os

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Change this to a random secure key

# Mock database of admin users (replace with your actual implementation)
users = {
    "admin1": generate_password_hash("admin1"),  # Replace 'hashed_password1' with actual hashed password
    "admin2": generate_password_hash("admin2")   # Replace 'hashed_password2' with actual hashed password
}

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, 'data/roster.db')

def create_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            UFID TEXT NOT NULL,
            ISO TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            class1 TEXT,
            class2 TEXT,
            class3 TEXT,
            class4 TEXT,
            class5 TEXT,
            class6 TEXT,
            class7 TEXT,
            class8 TEXT,
            PRIMARY KEY (UFID, ISO)
        )
    ''')

    conn.commit()
    conn.close()

def add_student(UFID, ISO, first_name, last_name, *classes):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the student already exists
    cursor.execute("SELECT * FROM student WHERE UFID = ? AND ISO = ?", (UFID, ISO))
    existing_student = cursor.fetchone()

    # If the student already exists, update data
    if existing_student:
        cursor.execute("UPDATE student SET first_name=?, last_name=?, class1=?, class2=?, class3=?, class4=?, class5=?, class6=?, class7=?, class8=? WHERE UFID=? AND ISO=?", (first_name, last_name, *classes, UFID, ISO))
    else:
        # Insert data into the student table
        cursor.execute("INSERT INTO student (UFID, ISO, first_name, last_name, class1, class2, class3, class4, class5, class6, class7, class8) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (UFID, ISO, first_name, last_name, *classes))

    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return redirect(url_for('form'))

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        UFID = request.form.get('ufid')
        ISO = request.form.get('iso')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        classes = [
            request.form.get('class1') or None,
            request.form.get('class2') or None,
            request.form.get('class3') or None,
            request.form.get('class4') or None,
            request.form.get('class5') or None,
            request.form.get('class6') or None,
            request.form.get('class7') or None,
            request.form.get('class8') or None
        ]

        add_student(UFID, ISO, first_name, last_name, *classes)

        return redirect(url_for('form'))

@app.route('/form2', methods=['GET', 'POST'])
def form2():
    if request.method == 'POST':
        # Check if it's an AJAX request
        if request.is_json:
            data = request.get_json()
            course_ids = data.get('course_ids', [])
            # Fetch courses based on the course IDs
            courses = {course_id: fetch_courses(course_id) for course_id in course_ids if course_id}
            #print(courses)
            return jsonify(courses)  # Return the courses as JSON

        # Handle standard form submission
        course_ids = [
            request.form.get(f'courseId{i}') for i in range(1, 9)
        ]
        courses = {course_id: fetch_courses(course_id) for course_id in course_ids if course_id}
        #print(courses)
        return render_template('form2.html', courses=courses)

    return render_template('form2.html', courses=None)

@app.route('/test_fetch_courses', methods=['GET'])
def test_fetch_courses():
    course_code = "COP"  # Example course code
    try:
        courses = fetch_courses(course_code=course_code)  # Call fetch_courses
        return jsonify(courses)  # Return the result as JSON for testing
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return the error as JSON

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('roster', page=1))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('form'))

@app.route('/timesheet')
def timesheet():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('timesheet.html')

@app.route('/roster', methods=['GET', 'POST'])
def roster():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        UFID = request.form.get('ufid')
        ISO = request.form.get('iso')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        classes = [
            request.form.get('class1') or None,
            request.form.get('class2') or None,
            request.form.get('class3') or None,
            request.form.get('class4') or None,
            request.form.get('class5') or None,
            request.form.get('class6') or None,
            request.form.get('class7') or None,
            request.form.get('class8') or None
        ]

        add_student(UFID, ISO, first_name, last_name, *classes)

        return redirect(url_for('roster', page=1))

    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of records per page

    conn = create_connection()
    cursor = conn.cursor()
    # Fetch total count of students
    cursor.execute("SELECT COUNT(*) FROM student")
    total_count = cursor.fetchone()[0]
    # Calculate total pages and adjust page if out of bounds
    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)
    page = min(page, total_pages)
    # Fetch students for the current page
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM student LIMIT ? OFFSET ?", (per_page, offset))
    students = cursor.fetchall()
    conn.close()

    return render_template('roster.html', students=students, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True)

