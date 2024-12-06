# ======================================================== #
#                IMPORTS AND CONFIGURATION                 #
# ======================================================== #
# Essential libraries and configurations for the application.

from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sqlcipher3
import os

# ======================================================== #
#                     APPLICATION SETUP                    #
# ======================================================== #
# Set up the Flask application, load environment variables,
# and configure session and encryption settings.

# Set the base directory for file paths and load environment variables
BASE_DIR = os.path.abspath(os.path.dirname(__file__))                           # Base directory
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))                         # Load environment variables from .env file

# Initialize Flask application
app = Flask(__name__)

# Configure application settings
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_fallback')    # Secret key for session management
app.config['ENCRYPTION_KEY'] = os.getenv('ENCRYPTION_KEY', 'default_fallback')  # Key for encrypting the database
app.config['SESSION_COOKIE_EXPIRES'] = None                                     # Set session cookie to expire when the browser is closed
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)                # 15 minutes session expiration
SESSION_TIMEOUT = timedelta(minutes=15)

# Mock database for admin users
users = {
    "admin1": generate_password_hash("admin1"),                                 # Replace 'hashed_password1' with actual hashed password
    "admin2": generate_password_hash("admin2")                                  # Replace 'hashed_password2' with actual hashed password
}

# Database file paths
DATABASE = os.path.join(BASE_DIR, 'data/roster.db')                             # Main database with student data, kiosks, and timesheet information
COURSE_DATA = os.path.join(BASE_DIR, 'data/courses_2248.db')                    # Courses database
EXAM_DATA = os.path.join(BASE_DIR, 'data/exams_2248.db')                        # Exams database
ENCRYPTED_DATABASE = os.path.join(BASE_DIR, 'data/roster_encrypted.db')         # Encrypted version of the main database

# Ensure the required data directory exists
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# ======================================================== #
#                    DATA INITIALIZATION                   #
# ======================================================== #
# Initialize databases and ensure all required tables exist.

# Initialize the unencrypted database with tables if it doesn't exist
def initialize_database():
    if not os.path.exists(DATABASE):
        conn = sqlcipher3.connect(DATABASE)
        cursor = conn.cursor()

        # Create the 'student' table
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

        # Create the 'PiConfig' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PiConfig (
                serial_num TEXT NOT NULL,
                room_num TEXT NOT NULL,
                PRIMARY KEY (serial_num)
            )
        ''')

        # Create the 'timesheet' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timesheet (
                UFID TEXT NOT NULL,
                ISO TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                course TEXT NOT NULL,
                class TEXT NOT NULL,
                instructor TEXT NOT NULL,
                room_num TEXT NOT NULL,
                time TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# ======================================================== #
#                    DATABASE ENCRYPTION                   #
# ======================================================== #
# Encrypt or re-encrypt the database to ensure data security.

# Encrypt the database if not already encrypted
def encrypt_existing_database():
    if not os.path.exists(ENCRYPTED_DATABASE): # Only encrypt if no encrypted version exists
        try:
            conn = sqlcipher3.connect(DATABASE)
            conn.execute(f"ATTACH DATABASE '{ENCRYPTED_DATABASE}' AS encrypted KEY '{app.config['ENCRYPTION_KEY']}'")
            conn.execute("SELECT sqlcipher_export('encrypted')")
            conn.execute("DETACH DATABASE encrypted")
            conn.close()
            os.replace(ENCRYPTED_DATABASE, DATABASE)
            print("Database encrypted successfully.")
        except Exception as e:
            print(f"Error during encryption: {e}")

# Re-encrypt the database by generating a fresh encrypted file
def re_encrypt_database():
    if os.path.exists(ENCRYPTED_DATABASE):
        os.remove(ENCRYPTED_DATABASE)

    try:
        # Open the unencrypted database
        conn = sqlcipher3.connect(DATABASE)
        # Attach and encrypt the new database
        conn.execute(f"ATTACH DATABASE '{ENCRYPTED_DATABASE}' AS encrypted KEY '{app.config['ENCRYPTION_KEY']}'")
        conn.execute("SELECT sqlcipher_export('encrypted')")
        conn.execute("DETACH DATABASE encrypted")
        conn.close()
        # Replace the original database file with the encrypted one
        os.replace(ENCRYPTED_DATABASE, DATABASE)
        print("Database re-encrypted successfully.")
    except Exception as e:
        print(f"Error during re-encryption: {e}")

# Custom exception for handling invalid encryption keys
class InvalidEncryptionKeyError(HTTPException):
    code = 403
    description = "The encryption password provided is incorrect. Please verify and try again."

    def get_response(self, environ=None):
        # Customize the JSON response
        response = jsonify({
            "error": "Invalid encryption key",
            "message": self.description
        })
        response.status_code = self.code
        return response

# ======================================================== #
#                    BACKEND FUNCTIONS                     #
# ======================================================== #
# Core utility functions for database operations, including
# initialization, encryption, and managing student or kiosk data.

# Create a connection to the database with encryption key validation
def create_connection():
    try:
        # Attempt to create a connection and set the encryption key
        conn = sqlcipher3.connect(DATABASE)
        conn.execute(f"PRAGMA key = '{app.config['ENCRYPTION_KEY']}'")

        # Test if the key is correct by querying the database
        conn.execute("SELECT COUNT(*) FROM sqlite_master;")

        return conn
    except sqlcipher3.DatabaseError:
        # Raise custom HTTPException with JSON response if the key is incorrect
        raise InvalidEncryptionKeyError

# Run database initialization and encryption at startup
initialize_database()
encrypt_existing_database()

# Function to add student's information into the database
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

# Function to add or update a kiosk
def add_or_update_kiosk(serial_num, room_num):
    conn = create_connection()
    try:
        cursor = conn.cursor()

        # Check if the student already exists
        cursor.execute("SELECT room_num FROM PiConfig WHERE serial_num = ?", (serial_num,))
        existing_kiosk = cursor.fetchone()

        # If the student already exists, update data
        if existing_kiosk:
            cursor.execute("UPDATE PiConfig SET room_num = ? WHERE serial_num = ?", (room_num, serial_num))
        else:
            # Insert data into the student table
            cursor.execute("INSERT INTO PiConfig (serial_num, room_num) VALUES (?, ?)", (serial_num, room_num))

        conn.commit() # Save changes to the database
    except sqlcipher3.Error as e:
        print(f"An error occurred: {e.args[0]}")
    finally:
        conn.close()

# ======================================================== #
#                    ROUTING ENDPOINTS                     #
# ======================================================== #
# Flask routes that handle HTTP requests, including user
# authentication, form submissions, and database management.

# Route for the home page, redirects users to the login page
@app.route('/')
def home():
    return redirect(url_for('login'))

# Route to handle the form page for adding student data
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

# Middleware function to check session timeout before every request
@app.before_request
def before_request():
    if 'logged_in' in session:
        # Check if the session has timed out
        last_activity = session.get('last_activity')
        if last_activity:
            try:
                last_activity_time = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S')
                if datetime.now() - last_activity_time > SESSION_TIMEOUT:
                    # Session has expired
                    session.clear()
                    return redirect(url_for('login'))
            except ValueError:
                # Handle incorrect datetime format
                session.clear()
                flash('Session information was invalid, please log in again.')
                return redirect(url_for('login'))

        # Update last activity time
        session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Route for login functionality
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            session['user'] = username  # Store user in session
            session['logged_in'] = True  # Flag to check if logged in
            session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Set last activity time
            return redirect(url_for('roster', page=1))
        else:
            flash('Invalid credentials')
            return redirect(url_for('login'))
    return render_template('login.html')

# Route for logout functionality
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

# Route to manage the timesheet
@app.route('/timesheet', methods=['GET', 'POST'])
def timesheet():
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Number of records per page

    conn = create_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Retrieve parameters from the URL
        serial_num = request.args.get('serial_num')
        ufid = request.args.get('ufid')
        iso = request.args.get('iso')
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        course = request.args.get('course')
        class_num = request.args.get('class')
        instructor = request.args.get('instructor')
        room_num = request.args.get('room_num')
        time = request.args.get('time')

        cursor.execute("SELECT * FROM PiConfig WHERE serial_num = ?", (serial_num,))
        kiosk = cursor.fetchone()

        print(kiosk)

        if kiosk:
            if all([ufid, iso, first_name, last_name, course, class_num, instructor, room_num, time]):
                # Insert data into the timesheet table
                cursor.execute('''
                    INSERT INTO timesheet (UFID, ISO, first_name, last_name, course, class, instructor, room_num, time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (ufid, iso, first_name, last_name, course, class_num, instructor, room_num, time))
                conn.commit()
                conn.close()
                return "Timesheet entry successfully added", 201
            else:
                conn.close()
                return "Missing data parameters", 400
        else:
            # Serial number does not exist in the kiosks table
            conn.close()
            return "Invalid serial number", 400

    # If GET request, show the timesheet records in the HTML table
    cursor.execute('SELECT COUNT(*) FROM timesheet')
    total_count = int(cursor.fetchone()[0])

    # Calculate total pages and adjust page if out of bounds
    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)
    page = min(page, total_pages)

    # Fetch timesheet data for the current page
    offset = (page - 1) * per_page
    cursor.execute("SELECT * FROM timesheet ORDER BY time DESC LIMIT ? OFFSET ?", (per_page, offset))
    timesheet_data = cursor.fetchall()

    conn.close()

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('timesheet.html', timesheet_data=timesheet_data, page=page, total_pages=total_pages)

# Route to manage the timesheet
@app.route('/timesheet/data', methods=['GET'])
def get_timesheet_data():
    conn = create_connection()
    cursor = conn.cursor()

    # Fetch all data from the timesheet table
    cursor.execute('SELECT * FROM timesheet')
    timesheet_data = cursor.fetchall()
    conn.close()

    # Return the raw data as JSON
    return jsonify(timesheet_data), 200

# Route to delete all timesheets
@app.route('/timesheet_delete_all', methods=['POST'])
def timesheet_delete_all():
    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Delete all entries from the Timesheet table
        cursor.execute("DELETE FROM timesheet")
        conn.commit()
        return jsonify({'success': True, 'message': 'All entries deleted successfully'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

    finally:
        conn.close()

# Route to manage student roster
@app.route('/roster', methods=['GET', 'POST'])
def roster():
    serial_num = request.args.get('serial_num')

    if serial_num:  # External API request logic
        if request.method == 'GET':
            # Handle external GET request by serial number
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT room_num FROM PiConfig WHERE serial_num = ?", (serial_num,))
            result = cursor.fetchone()
            conn.close()

            if result:
                # Serial number exists, check ufid or iso
                UFID = request.args.get('ufid')
                ISO = request.args.get('iso')

                if UFID or ISO:
                    # Perform additional checks here
                    conn = create_connection()  # Reconnect if needed
                    cursor = conn.cursor()
                    if UFID:
                        cursor.execute("SELECT * FROM student WHERE UFID = ?", (UFID,))
                    elif ISO:
                        cursor.execute("SELECT * FROM student WHERE ISO = ?", (ISO,))
                    student_result = cursor.fetchone()
                    conn.close()

                    if student_result:
                        return jsonify({"student_data": student_result})
                    else:
                        return jsonify({"error": "UFID or ISO not found"}), 404

                # Remove this line if not needed
                return jsonify({"error": "Serial number exists but no additional parameters provided"}), 400
            else:
                return jsonify({"error": "Serial number not found"}), 404

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

# Route to delete students inside student database
@app.route('/roster_delete', methods=['POST'])
def delete_student():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    data = request.get_json()
    ufid = data.get('ufid')
    iso = data.get('iso')

    if not ufid or not iso:
        return jsonify({'success': False, 'message': 'UFID and ISO are required'}), 400

    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM student WHERE UFID = ? AND ISO = ?", (ufid, iso))
        conn.commit()
        return jsonify({'success': True, 'message': 'Student deleted successfully'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        conn.close()

# Route to manage all kiosks
@app.route('/kiosks', methods=['GET'])
def kiosks():
    serial_num = request.args.get('serial_num')

    if serial_num:  # External API request logic
        if request.method == 'GET':
            # Handle external GET request by serial number
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT room_num FROM PiConfig WHERE serial_num = ?", (serial_num,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return jsonify({"room_num": result[0]})
            else:
                return jsonify({"error": "Serial number not found"}), 404

    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    # Get the page number from the query string, default to 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Set the number of records per page

    conn = create_connection()
    cursor = conn.cursor()

    # Get total number of kiosks
    cursor.execute("SELECT COUNT(*) FROM PiConfig")
    total_count = cursor.fetchone()[0]

    # Calculate the offset for SQL query
    offset = (page - 1) * per_page

    # Fetch the kiosks for the current page
    cursor.execute("SELECT * FROM PiConfig LIMIT ? OFFSET ?", (per_page, offset))
    kiosks = cursor.fetchall()

    conn.close()

    # Calculate total pages
    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)

    return render_template('kiosks.html', kiosks=kiosks, page=page, total_pages=total_pages)

# Route to add kiosks into kiosk table
@app.route('/add_kiosk', methods=['POST'])
def add_kiosk():
    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    app.logger.info(f'User {session["user"]} is adding a kiosk')

    # Get JSON data from the request
    if request.is_json:
        data = request.get_json()
        serial_num = data.get('serialNumber')
        room_num = data.get('classroom')
    else:
        return jsonify({'success': False, 'message': 'Request must be JSON'}), 400

    # Validate the inputs
    if not serial_num or not room_num:
        return jsonify({'success': False, 'message': 'Missing serial number or room number'})

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if the kiosk exists; if it does, update it
        cursor.execute("SELECT serial_num FROM PiConfig WHERE serial_num = ?", (serial_num,))
        existing_kiosk = cursor.fetchone()

        if existing_kiosk:
            # If the kiosk exists, update the classroom
            cursor.execute("UPDATE PiConfig SET room_num = ? WHERE serial_num = ?", (room_num, serial_num))
        else:
            # If it doesn't exist, insert the new kiosk
            cursor.execute("INSERT INTO PiConfig (serial_num, room_num) VALUES (?, ?)", (serial_num, room_num))

        conn.commit()
        return jsonify({'success': True, 'message': 'Kiosk added or updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to add or update kiosk: {str(e)}'})
    finally:
        conn.close()

# Route to update kiosks in the case they are edited
@app.route('/update_kiosks', methods=['POST'])
def update_pi():
    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    data = request.get_json()
    old_serial = data['oldSerial']
    new_serial = data['newSerial']
    room_num = data['room_num']

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Check if we are actually changing the serial number
        if old_serial != new_serial:
            # Remove any unique constraint errors by updating the serial number and room number
            cursor.execute("UPDATE PiConfig SET serial_num = ?, room_num = ? WHERE serial_num = ?", (new_serial, room_num, old_serial))
        else:
            # Just update the room number if the serial number remains the same
            cursor.execute("UPDATE PiConfig SET room_num = ? WHERE serial_num = ?", (room_num, old_serial))

        conn.commit()
        return jsonify({'success': True, 'message': 'Kiosk updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to update kiosk: {str(e)}'})
    finally:
        conn.close()

# Route to delete a kiosk
@app.route('/delete_kiosks', methods=['POST'])
def delete_pi():
    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    data = request.get_json()
    serial_num = data['serial_num']

    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM PiConfig WHERE serial_num = ?", (serial_num,))
        conn.commit()
        return jsonify({'success': True, 'message': 'Pi deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

# Route to delete all kiosks
@app.route('/delete_all_kiosks', methods=['POST'])
def delete_all_kiosks():
    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    conn = create_connection()
    cursor = conn.cursor()
    try:
        # Delete all entries from the PiConfig table
        cursor.execute("DELETE FROM PiConfig")
        conn.commit()
        return jsonify({'success': True, 'message': 'All kiosks deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    finally:
        conn.close()

# Route to fetch all kiosks data from kiosk database
@app.route('/all_kiosks', methods=['GET'])
def all_kiosks():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM PiConfig")
    kiosks = cursor.fetchall()
    conn.close()
    return jsonify(kiosks)

# Route to manage courses
@app.route('/courses', methods=['GET'])
def courses():
    if request.method == 'GET':
        # Get parameters from the request
        day = request.args.get('day')  # Get a single value for 'day'
        roomCode = request.args.get('roomCode')

        # Check if day is provided
        if not day or day not in ['M', 'T', 'W', 'R', 'F', 'S']:
            return jsonify({"error": "Invalid or no day provided"}), 400

        # Connect to the database
        conn = sqlcipher3.connect(COURSE_DATA)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM courses WHERE meet_days LIKE ? AND meet_room_code = ?", (f'%{day}%', roomCode))

        # Fetch the relevant courses
        courses = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Return the results as JSON
        return jsonify(courses)

# Route to manage exams
@app.route('/exams', methods=['GET'])
def exams():
    serial_num = request.args.get('serial_num')
    date = request.args.get('date')

    if serial_num:  # External API request logic
        if request.method == 'GET':
            # Handle external GET request by serial number
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT room_num FROM PiConfig WHERE serial_num = ?", (serial_num,))
            result = cursor.fetchone()
            conn.close()

            if result:
                room = result[0]  # Store the room number from the PiConfig table

                # Now, find all courses with that room number
                conn = sqlcipher3.connect(EXAM_DATA)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM courses WHERE room = ? AND date = ?", (room, date))
                courses = cursor.fetchall()  # Get all matching courses

                conn.close()

                return jsonify(courses)

            else:
                return jsonify({"error": "Serial number not found"}), 404

    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    # Get the page number from the query string, default to 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Set the number of records per page

    conn = sqlcipher3.connect(EXAM_DATA)
    cursor = conn.cursor()

    # Get total number of kiosks
    cursor.execute("SELECT COUNT(*) FROM courses")
    total_count = cursor.fetchone()[0]

    # Calculate the offset for SQL query
    offset = (page - 1) * per_page

    # Fetch the kiosks for the current page
    cursor.execute("SELECT * FROM courses LIMIT ? OFFSET ?", (per_page, offset))
    exams = cursor.fetchall()

    conn.close()

    # Calculate total pages
    total_pages = (total_count // per_page) + (1 if total_count % per_page > 0 else 0)

    return render_template('exams.html', exams=exams, page=page, total_pages=total_pages)

# Route to update exams in case they are edited
@app.route('/update_exams', methods=['POST'])
def update_exams():
    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    data = request.get_json()
    course_code = data['courseCode']
    course_name = data['courseName']
    room_num = data['room']
    date = data['date']
    start_time = data['start']
    end_time = data['end']

    conn = sqlcipher3.connect(EXAM_DATA)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            UPDATE courses SET room = ?, date = ?, start_time = ?, end_time = ? WHERE course_code = ? AND course_name = ?
        ''', (room_num if room_num is not None else None,
              date if date is not None else None,
              start_time if start_time is not None else None,
              end_time if end_time is not None else None,
              course_code, course_name))

        conn.commit()
        return jsonify({'success': True, 'message': 'Exam updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to update exam: {str(e)}'})
    finally:
        conn.close()

# Route to fetch all exam data from exam database
@app.route('/all_exams', methods=['GET'])
def all_exams():
    if 'logged_in' not in session and request.endpoint not in ['login', 'form']:
        return redirect(url_for('login'))

    conn = sqlcipher3.connect(EXAM_DATA)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    exams = cursor.fetchall()
    conn.close()
    return jsonify(exams)

# ======================================================== #
#                     TESTING ROUTES                       #
# ======================================================== #
# Routes used for testing application functionality, including
# encryption validation and basic connectivity checks.

@app.route('/index', methods=['GET'])
def index():
    if request.method == 'GET':
        return "Hello World"

@app.route('/success')
def success():
    return "File uploaded successfully!"

# Example endpoint to test encrypted connection
@app.route('/encryption_test')
def encryption_test():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS example (id INTEGER PRIMARY KEY, data TEXT);")
        cursor.execute("INSERT OR IGNORE INTO example (id, data) VALUES (1, 'Hello, encrypted world!');")
        cursor.execute("SELECT * FROM example")
        example_data = cursor.fetchall()
        conn.commit()
        conn.close()
        return jsonify({"decrypted_example_data": example_data})
    except sqlcipher3.DatabaseError as e:
        return jsonify({"error": str(e)})

@app.route('/verify_encryption')
def verify_encryption():
    try:
        conn = sqlcipher3.connect(DATABASE)
        conn.execute(f"PRAGMA key = '{app.config['ENCRYPTION_KEY']}'")  # Directly insert the key
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM sqlite_master;")  # Test query to check if the database is accessible
        result = cursor.fetchone()
        conn.close()
        return jsonify({"status": "Encryption key valid", "result": result})
    except sqlcipher3.DatabaseError as e:
        return jsonify({"error": "Invalid encryption key or database issue", "details": str(e)})

# Entry point of the application
if __name__ == '__main__':
    re_encrypt_database()
    app.run(debug=True)

