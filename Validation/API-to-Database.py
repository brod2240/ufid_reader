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

        if existing_entry:
            # Print details of the existing entry and the new duplicate
            print(f"Duplicate found:")
            #print(f"Existing entry - Class Number: {class_number}, Course Code: {existing_entry[0]}")
            #print(f"New entry - Class Number: {class_number}, Course Code: {course_code}")
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO courses (course_code, class_number, instructors, meet_no, meet_days, meet_time_begin, meet_time_end, meet_room_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (code, classNumber, instructor, meetNo, meetDays, meetTimeBegin, meetTimeEnd, meetRoomCode))

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
