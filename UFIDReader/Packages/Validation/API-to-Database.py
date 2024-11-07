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
                            'meetRoomCode': roomCode
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_code TEXT,
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
                INSERT INTO courses (course_code, class_number, instructors, meet_no, meet_days, meet_time_begin, meet_time_end, meet_room_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (code, classNumber, instructor, meetNo, meetDays, meetTimeBegin, meetTimeEnd, meetRoomCode))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def prof_profile(db_name, term):
    # Step 1: Connect to the Database
    conn = sqlite3.connect(db_name)  # Replace with your database filename
    cursor = conn.cursor()

    # Step 2: Query the Data
    query = '''
    SELECT instructors, course_code, class_number
    FROM courses
    ORDER BY instructors, course_code, class_number
    '''
    cursor.execute(query)
    rows = cursor.fetchall()

    # Step 3: Organize Data by Individual Instructor with Unique Sections
    # Structure: { instructor: { course_code: set(section_number, ...) } }
    organized_data = {}

    for row in rows:
        instructor_field, course_code, section_number = row

        # Step 4: Split the instructor field into individual names
        instructors = [name.strip() for name in instructor_field.split(',')]

        for instructor in instructors:
            # Initialize dictionary structure if not already present for the instructor
            if instructor not in organized_data:
                organized_data[instructor] = {}

            # Initialize set for course code if not already present
            if course_code not in organized_data[instructor]:
                organized_data[instructor][course_code] = set()

            # Add the section number to the course code set (automatically ensures uniqueness)
            organized_data[instructor][course_code].add(section_number)

    # Step 5: Convert sets to lists for JSON serialization
    for instructor, courses in organized_data.items():
        for course_code in courses:
            organized_data[instructor][course_code] = list(courses[course_code])

    # Step 6: Output the Data
    with open(f'organized_courses_{term}.json', 'w') as f:
        json.dump(organized_data, f, indent=4)

    # Close the connection
    conn.close()

    print("Data organized with unique sections and saved to organized_courses.json")

def main():
    term = input("Enter the term (e.g., 1, 6W1, 6W2): ")
    db_name = f"courses_{term}.db"

    course_data = fetch_courses(term)
    save_to_db(db_name, course_data)
    prof_profile(db_name, term)

    print(f"\nData successfully saved to {db_name}")

if __name__ == "__main__":
    main()
