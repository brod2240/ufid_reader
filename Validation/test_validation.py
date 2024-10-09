from datetime import datetime, timedelta
import requests

def web_api_get_request(page, params):
    url = "https://gatorufid.pythonanywhere.com/"
    url += page
    response = requests.get(url, params=params)

    return response    

def validate(serial_num, card_iso=None, card_ufid=None):
    params = {
        "serial_num": serial_num,
        "iso": card_iso,
        "ufid": card_ufid
    }

    student = web_api_get_request(page="roster", params=params)

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
                #print(student_sec_num)
                #do post request to timesheet
                url = "https://gatorufid.pythonanywhere.com/timesheet"
                response = requests.post(url, params=params)
                #print(response)

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
valid = validate("10000000d340eb60", card_ufid="20000000")
print(valid)
#valid = validate("10000000d340eb60", card_ufid="77211373")
#print(valid)
