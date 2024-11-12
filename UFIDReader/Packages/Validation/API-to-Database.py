'''
import requests

url = "https://one.ufl.edu/apix/soc/schedule/"

term = 2248

# Initialize query parameters
params = {
    "category": "CWSP",
    "term": term,  # Adjusted to the term you specified 6W1 for A. 6W2 for B. 1 for C
    "last-control-number": 0,
}

response = requests.get(url, params=params)
#response = requests.get(url)

#print(response)

# Check if the request was successful
if response.status_code == 200:
    
    results = []
    #print(response)
    data = response.json()
    #print(data)

    courses = data[0].get('COURSES', [])
    retrievedrows = data[0].get('RETRIEVEDROWS', 0)
    lastcontrolnumber = data[0].get('LASTCONTROLNUMBER', 0)

    for course in courses:
        code = course.get('code')
        #print(code)
        for section in course.get('sections', []):
            class_number = section.get('classNumber')
            instructors = ', '.join([instructor['name'] for instructor in section['instructors']])
            for time in section['meetTimes']:
                meetNum = time['meetNo']
                meet_time_begin = time['meetTimeBegin']
                meet_time_end = time['meetTimeEnd']
                roomCode = time['meetBuilding'] + str(time['meetRoom'])  # Combine building and room
                meetDays = time['meetDays']
                results.append({
                    'code': code,
                    'classNumber': class_number,
                    'instructor(s)': instructors,
                    'meetNo': meetNum,
                    'meetDays': meetDays,
                    'meetTimeBegin': meet_time_begin,
                    'meetTimeEnd': meet_time_end,
                    'meetRoomCode': roomCode
                })
    print(results)
'''

import requests
import sqlite3
import sys
import json

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
    total_sections = 0  # Counter for the number of courses processed

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
                course_name = course.get('name')
                sections = course.get('sections', [])
                for section in sections:
                    class_number = section.get('classNumber')
                    instructors = ', '.join([instructor['name'] for instructor in section['instructors']])
                    for time in section['meetTimes']:
                        meetNum = time['meetNo']
                        meet_time_begin = time['meetTimeBegin']
                        meet_time_end = time['meetTimeEnd']
                        roomCode = time['meetBuilding'] + str(time['meetRoom'])  # Combine building and room
                        meetDays = time['meetDays']
                        
                        course_results.append({
                            'code': course_code,
                            'classNumber': class_number,
                            'instructor(s)': instructors,
                            'meetNo': meetNum,
                            'meetDays': meetDays,
                            'meetTimeBegin': meet_time_begin,
                            'meetTimeEnd': meet_time_end,
                            'meetRoomCode': roomCode,
                            'name': course_name
                        })

                    # Update the progress indicator
                    total_sections += 1
                    sys.stdout.write(f"\rSections loaded: {total_sections}")
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

    cursor.execute('DROP TABLE IF EXISTS courses')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT,
            course_name TEXT,
            class_number TEXT,
            instructors TEXT,
            meet_no TEXT,
            meet_days TEXT,
            meet_time_begin TEXT,
            meet_time_end TEXT,
            meet_room_code TEXT,
            PRIMARY KEY (class_number, meet_no)
        )
    ''')

    for course in course_data:
        code = course["code"]
        name = course["name"]
        classNumber = course["classNumber"]
        instructor = course["instructor(s)"]
        meetNo = course["meetNo"]
        meetDays = str(course["meetDays"])
        meetTimeBegin = course["meetTimeBegin"]
        meetTimeEnd = course["meetTimeEnd"]
        meetRoomCode = course["meetRoomCode"]

        # Check if the class_number already exists in the database
        cursor.execute('''
            SELECT * FROM courses WHERE class_number = ? AND meet_no = ?
        ''', (classNumber, meetNo))
        
        existing_entry = cursor.fetchone()

        if not existing_entry:
            # Print details of the existing entry and the new duplicate
            #print(f"Duplicate found:")
            #print(f"Existing entry - Class Number: {class_number}, Course Code: {existing_entry[0]}")
            #print(f"New entry - Class Number: {class_number}, Course Code: {course_code}")
        #else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO courses (course_code, course_name, class_number, instructors, meet_no, meet_days, meet_time_begin, meet_time_end, meet_room_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (code, name, classNumber, instructor, meetNo, meetDays, meetTimeBegin, meetTimeEnd, meetRoomCode))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def prof_profile(db_name, term):
    # Step 1: Connect to the Database
    conn = sqlite3.connect(db_name)  # Replace with your database filename
    cursor = conn.cursor()

    # Step 2: Query the Data
    query = '''
    SELECT instructors, course_code, course_name, class_number
    FROM courses
    ORDER BY instructors, course_code, course_name, class_number
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Step 3: Organize Data by Instructor -> Course Code + Course Name -> Section Number
    # Structure: { instructor: { "course_code: course_name": set(section_number, ...) } }
    organized_data = {}

    for row in rows:
        instructor_field, course_code, course_name, section_number = row

        # Step 4: Split the instructor field into individual names
        instructors = [name.strip() for name in instructor_field.split(',')]

        for instructor in instructors:
            # Initialize dictionary structure if not already present for the instructor
            if instructor not in organized_data:
                organized_data[instructor] = {}

            # Combine course code and course name
            course_key = f"{course_code}: {course_name}"

            # Initialize set for course if not already present
            if course_key not in organized_data[instructor]:
                organized_data[instructor][course_key] = set()

            # Add the section number to the course set (automatically ensures uniqueness)
            organized_data[instructor][course_key].add(section_number)

    # Step 5: Convert sets to lists for JSON serialization
    for instructor, courses in organized_data.items():
        for course_key in courses:
            organized_data[instructor][course_key] = list(courses[course_key])

    # Step 6: Output the Data
    with open(f'organized_courses_{term}.json', 'w') as f:
        json.dump(organized_data, f, indent=4)

    # Close the connection
    conn.close()

    print(f"Data organized with unique sections and saved to organized_courses_{term}.json")

def exam_database(db_name, exam_db_name):
    source_conn = sqlite3.connect(db_name)
    source_cursor = source_conn.cursor()

    # Connect to the new database
    new_conn = sqlite3.connect(exam_db_name)
    new_cursor = new_conn.cursor()

    # Create the new table with the specified fields
    new_cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT,
            course_name TEXT,
            instructors TEXT,
            sections TEXT,
            room TEXT DEFAULT NULL,
            date TEXT DEFAULT NULL,
            start_time TEXT DEFAULT NULL,
            end_time TEXT DEFAULT NULL,
            PRIMARY KEY (course_code, course_name)
        )
    ''')

    # Query to retrieve all relevant data from the source database
    source_cursor.execute('''
        SELECT 
            course_code, 
            course_name, 
            instructors, 
            class_number
        FROM courses
    ''')

    # Use a dictionary to collect unique instructors and sections for each course
    course_data = {}

    for row in source_cursor.fetchall():
        course_code, course_name, instructor, section = row
        key = (course_code, course_name)

        # Initialize the entry in the dictionary if it doesn't exist
        if key not in course_data:
            course_data[key] = {"instructors": set(), "sections": set()}

        # Add instructors and sections to the sets (automatically handles duplicates)
        course_data[key]["instructors"].add(instructor)
        course_data[key]["sections"].add(section)

    # Insert the processed data into the new database
    for (course_code, course_name), data in course_data.items():
        instructors = ', '.join(data["instructors"])  # Convert sets to comma-separated strings
        sections = ', '.join(data["sections"])

        new_cursor.execute('''
            INSERT INTO courses (course_code, course_name, instructors, sections)
            VALUES (?, ?, ?, ?)
        ''', (course_code, course_name, instructors, sections))

    # Commit the changes and close the connections
    new_conn.commit()
    source_conn.close()
    new_conn.close()

def main():
    term = input("Enter the term (e.g., 1, 6W1, 6W2): ")
    db_name = f"courses_{term}.db"
    exam_db_name = f"exams_{term}.db"

    course_data = fetch_courses(term)
    save_to_db(db_name, course_data)
    prof_profile(db_name, term)

    exam_database(db_name, exam_db_name)

    print(f"\nData successfully saved to {db_name}")

if __name__ == "__main__":
    main()
