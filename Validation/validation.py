from datetime import datetime, timedelta
import requests
import json
import urllib.parse


def web_api_get_request(page, params):
    url = "https://gatorufid.pythonanywhere.com/"
    url += page
    response = requests.get(url, params=params)

    return response
    # Check if the request was successful
    #if response.status_code == 200:
    #    data = response.json()
    #return data


'''
def fetch_courses(time, day, room, course_code=None, class_num=None, day_m=None, day_t=None, day_w=None, day_r=None, day_f=None, day_s=None, instructor=None):
    # URL to send the GET request to
    url = "https://one.ufl.edu/apix/soc/schedule/"

    #term = get_term()

    # Initialize query parameters
    params = {
        "category": "CWSP",
        "term": 2248,  # Adjusted to the term you specified 6W1 for A. 6W2 for B. 1 for C #CHANGE HARDCODE
        "last-control-number": 0,
    }

    # Add course_code and class_num to params if provided
    if course_code:
        params["course-code"] = course_code
    if class_num:
        params["class-num"] = class_num
    if day_m:
        params["day-m"] = day_m
    if day_t:
        params["day-t"] = day_t
    if day_w:
        params["day-w"] = day_w
    if day_r:
        params["day-r"] = day_r
    if day_f:
        params["day-f"] = day_f
    if day_s:
        params["day-s"] = day_s    
    if instructor:
        params["instructor"] = instructor

    course_results = []
    start = 1

    while True:
        # Send the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Assuming the response contains a dictionary with a 'courses' key
            courses = data[0]['COURSES']  # Use .get() for safe access
            retrievedrows = data[0]['RETRIEVEDROWS']
            lastcontrolnumber = data[0]['LASTCONTROLNUMBER']
            #totalrows = data[0]['TOTALROWS']

            if retrievedrows == 0 and lastcontrolnumber == 0:
                break

            # Iterate through each course in the courses list
            for i, course in enumerate(courses, start):
                course_code = course.get('code')
                sections = course.get('sections', [])
                #print(sections)

                # Iterate through each section in the sections list
                for section in sections:
                    class_number = section.get('classNumber')  # Extracts class number
                    # print(course_code, " ", class_number)
                    instructors = section.get('instructors') # Extracts instructor
                    meetingTimes = section.get('meetTimes') # Extracts meetTimes
        
                    # Iterates through each meetTime in meetTimes
                    for meetingTime in meetingTimes:
                        meetDays = meetingTime['meetDays'] # Extracts the meeting day

                        # Converts the meeting time to a time object
                        meetTimeBegin = meetingTime['meetTimeBegin']
                        begin_time_obj = datetime.datetime.strptime(meetTimeBegin, "%I:%M %p").time()
                        meetTimeEnd = meetingTime['meetTimeEnd']
                        end_time_obj = datetime.datetime.strptime(meetTimeEnd, "%I:%M %p").time()

                        building = meetingTime['meetBuilding']
                        roomNum = str(meetingTime['meetRoom'])
                        #print(building)
                        #print(roomNum)
                        roomCode = building + roomNum
                        #print(roomCode)
                        
                        if (day in meetDays) and (begin_time_obj <= time <= end_time_obj) and (room == roomCode): # Compares current time and day with that of class
                            #print("hello")
                            course_results.append({ # Appends results if in range
                                "index": i,
                                "course_code": course_code,
                                "class_number": class_number,
                                "instructors": instructors,
                                "meetTimeBegin" : meetTimeBegin,
                                "meetTimeEnd": meetTimeEnd
                            })
                            print(meetTimeBegin)
                            print(meetTimeEnd)
                    

            params['last-control-number'] = lastcontrolnumber
            start = i + 1

        else:
            print(f"Failed to retrieve data: {response.status_code}")

    return course_results
'''
    

def validate(serial_num, card_iso=None, card_ufid=None):
    params = {
        "serial_num": serial_num,
        "iso": card_iso,
        "ufid": card_ufid
    }

    student = web_api_get_request(page="roster", params=params)
    #print(student)

    if student.status_code != 200:
        if student.json()['error'] == "Serial number not found":
            return {
                "UFID": None,
                "First Name": None,
                "Last Name": None,
                "Valid": -1  # -1 indicates invalid serial number
            }

        if student.json()['error'] == "UFID or ISO not found":
            return {
                "UFID": None,
                "First Name": None,
                "Last Name": None,
                "Valid": -2  # -1 indicates invalid serial number
            }

    student = student.json()
    #print(student)

    student_sec_nums = [student['student_data'][i] for i in range(4, 12) if student['student_data'][i] is not None]

    #print(student_sec_nums)

    # Extract UFID, first name, and last name
    ufid = student['student_data'][0]
    iso = student['student_data'][1]
    first_name = student['student_data'][2]
    last_name = student['student_data'][3]

    # Initialize a validation as -3; validation ranges from 0 - -3;
    is_valid = -3

    params = {
        "serial_num": serial_num
    }
    #print(params)
    room = (web_api_get_request(page="kiosks", params=params)).json()['room_num']
    #print(room)
    #print(room)

    #now = datetime.now()
    now = datetime(2024, 9, 19, 11, 0, 0)

    day = now.weekday()

    actual_now = datetime.now() #for prof website post request

    current_time = now.time()
    #current_time = datetime.strptime('10:40 AM', '%I:%M %p')
    #current_time = now.strptime('10:40:00 AM', '%I:%M:%S %p')

    match day:
        case 0:  # Monday
            day = 'M'
        case 1:  # Tuesday
            day = 'T'
        case 2:  # Wednesday
            day = 'W'
        case 3:  # Thursday
            day = 'R'
        case 4:  # Friday
            day = 'F'
        case 5:  # Saturday
            day = 'S'
        case _:
            print("Invalid day")
        
    params = {
        "day": day,
        "roomCode": room
    }

    results = (web_api_get_request(page='courses', params=params)).json()

    #print(results)

    courses = []

    #print(current_time)

    for result in results:
        start = datetime.strptime(result[5], '%I:%M %p') - timedelta(minutes=15)
        end = datetime.strptime(result[6], '%I:%M %p') + timedelta(minutes=15) #possible change
        if start.time() <= current_time <= end.time():
            courses.append(result)


    #print(courses)

    for course in courses:
        course_sec_num = course[1]
        for student_sec_num in student_sec_nums:
            if course_sec_num == student_sec_num:
                params = {
                    'serial_num': serial_num, 
                    'ufid': ufid,
                    'iso': iso, 
                    'first_name': first_name, 
                    'last_name': last_name,
                    'course': course[0],
                    'class': course[1],
                    'instructor': course[2],
                    'room_num': course[7],
                    'time':  now.strftime("%m/%d/%Y %I:%M:%S %p")
                }

                checkin_site_params = {
                    'serial_num': serial_num, 
                    'ufid': ufid,
                    'iso': iso, 
                    'first_name': first_name, 
                    'last_name': last_name,
                    'course': course[0],
                    'class': course[1],
                    'instructor': course[2],
                    'room_num': course[7],
                    'time': actual_now.strftime("%Y-%m-%d %H:%M:%S")
                }

                #print(student_sec_num)
                #do post request to timesheet
                url = "https://gatorufid.pythonanywhere.com/timesheet"
                response = requests.post(url, params=params)

                checkin_web_url = "https://brirod2240.pythonanywhere.com/api/add_timesheet"
                site_response = requests.post(checkin_web_url, json=checkin_site_params)
                #print(site_response)
                #print(site_response.text)

                is_valid = 0


    #fetch_courses()

    validation = {
        "UFID": ufid,
        "First Name": first_name,
        "Last Name": last_name,
        "Valid": is_valid
    }

    return validation

#fetch_courses(course_code="CHM6586")
valid = validate("10000000d340eb60", card_ufid="77211373")
#print(valid)
