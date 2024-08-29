import requests
import sqlite3
import sys

def fetch_courses(term, course_code=None, class_num=None):
    # URL to send the GET request to
    url = "https://one.ufl.edu/apix/soc/schedule/"

    # Initialize query parameters
    params = {
        "category": "CWSP",
        "term": term,
        "last-control-number": 0
    }

    course_results = []
    total_courses = 0  # Counter for the number of courses processed

    while True:
        # Send the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            courses = data[0].get('COURSES', [])
            retrievedrows = data[0].get('RETRIEVEDROWS', 0)
            lastcontrolnumber = data[0].get('LASTCONTROLNUMBER', 0)

            if retrievedrows == 0 and lastcontrolnumber == 0:
                break

            # Iterate through each course in the courses list
            for course in courses:
                course_code = course.get('code')
                sections = course.get('sections', [])

                for section in sections:
                    class_number = section.get('classNumber')
                    course_results.append({
                        "course_code": course_code,
                        "class_number": class_number
                    })

                    # Update the progress indicator
                    total_courses += 1
                    sys.stdout.write(f"\rCourses loaded: {total_courses}")
                    sys.stdout.flush()

            params['last-control-number'] = lastcontrolnumber

        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break

    print()  # Move to the next line after loading is complete
    return course_results

def save_to_db(db_name, course_data):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            class_number TEXT PRIMARY KEY,
            course_code TEXT
        )
    ''')

    for course in course_data:
        class_number = course["class_number"]
        course_code = course["course_code"]

        # Check if the class_number already exists in the database
        cursor.execute('''
            SELECT course_code FROM courses WHERE class_number = ?
        ''', (class_number,))
        
        existing_entry = cursor.fetchone()

        if existing_entry:
            # Print details of the existing entry and the new duplicate
            print(f"Duplicate found:")
            print(f"Existing entry - Class Number: {class_number}, Course Code: {existing_entry[0]}")
            print(f"New entry - Class Number: {class_number}, Course Code: {course_code}")
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO courses (class_number, course_code)
                VALUES (?, ?)
            ''', (class_number, course_code))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def main():
    term = input("Enter the term (e.g., 1, 6W1, 6W2): ")
    db_name = f"courses_{term}.db"

    course_data = fetch_courses(term)
    save_to_db(db_name, course_data)

    print(f"\nData successfully saved to {db_name}")

if __name__ == "__main__":
    main()
