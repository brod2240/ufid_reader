from datetime import datetime, timedelta
import requests

def web_api_get_request(page, params):
    url = "https://gatorufid.pythonanywhere.com/"
    url += page
    response = requests.get(url, params=params, timeout=10)

    return response    

def validate(mode, serial_num, card_iso=None, card_ufid=None):
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
                "Valid": -2  # -2 indicates invalid UFID or ISO
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

    now = datetime.now()
    #now = datetime(2024, 9, 19, 11, 0, 0)

    date = now.strftime("%m/%d/%Y")

    day = now.weekday()

    #actual_now = datetime.now() #for prof website post request

    current_time = now.time()
    #current_time = datetime.strptime('10:40 AM', '%I:%M %p')
    #current_time = now.strptime('10:40:00 AM', '%I:%M:%S %p')
    #print(current_time)

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
            return {
                "UFID": None,
                "First Name": None,
                "Last Name": None,
                "Valid": -4  # -4 indicates not school day
            }
    #print(day)
    #print(room)
    #print()
        
    params1 = {
        "day": day,
        "roomCode": room
    }

    params2 = {
        "serial_num": serial_num,
        "date": date
    }

    if mode == 1:
        results = (web_api_get_request(page='exams', params=params2)).json()
    else:
        results = (web_api_get_request(page='courses', params=params1)).json()
    
    # What if no class in room on day??
    # Tested it with Saturday seems fine just registers as no match -3


    #print(results)
    #print(results)
    #print()

    courses = []

    #print(current_time)

    for result in results:
        #start = datetime.strptime(result[5], '%I:%M %p') - timedelta(minutes=15)
        #end = datetime.strptime(result[6], '%I:%M %p') + timedelta(minutes=15) #possible change
        if mode == 1:
            start = datetime.strptime(result[6], '%I:%M %p').replace(year=now.year, month=now.month, day=now.day) #- timedelta(minutes=15)
            end = datetime.strptime(result[7], '%I:%M %p').replace(year=now.year, month=now.month, day=now.day) #+ timedelta(minutes=15)
        else:
            start = datetime.strptime(result[6], '%I:%M %p').replace(year=now.year, month=now.month, day=now.day) - timedelta(minutes=15)
            end = datetime.strptime(result[7], '%I:%M %p').replace(year=now.year, month=now.month, day=now.day) + timedelta(minutes=15)
    
        #print(start)
        #print(current_time)
        #print(end)
        if start.time() <= current_time <= end.time():
            courses.append(result)


    #print(courses)

    if mode == 1:
        for course in courses:
            course_sec_nums = course[3].split(', ')
            for student_sec_num in student_sec_nums:
                if student_sec_num in course_sec_nums:
                    params = {
                        'serial_num': serial_num, 
                        'ufid': ufid,
                        'iso': iso, 
                        'first_name': first_name, 
                        'last_name': last_name,
                        'course': course[0],
                        'class': student_sec_num,
                        'instructor': course[2],
                        'room_num': course[4],
                        'time':  now.strftime("%m/%d/%Y %I:%M:%S %p")
                    }

                    checkin_site_params = {
                        'serial_num': serial_num, 
                        'ufid': ufid,
                        'iso': iso, 
                        'first_name': first_name, 
                        'last_name': last_name,
                        'course': course[0],
                        'class': student_sec_num,
                        'instructor': course[2],
                        'room_num': course[4],
                        'time': now.strftime("%Y-%m-%d %H:%M:%S")
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
    else:
        for course in courses:
            course_sec_num = course[2]
            for student_sec_num in student_sec_nums:
                if course_sec_num == student_sec_num:
                    params = {
                        'serial_num': serial_num, 
                        'ufid': ufid,
                        'iso': iso, 
                        'first_name': first_name, 
                        'last_name': last_name,
                        'course': course[0],
                        'class': course[2],
                        'instructor': course[3],
                        'room_num': course[8],
                        'time':  now.strftime("%m/%d/%Y %I:%M:%S %p")
                    }

                    checkin_site_params = {
                        'serial_num': serial_num, 
                        'ufid': ufid,
                        'iso': iso, 
                        'first_name': first_name, 
                        'last_name': last_name,
                        'course': course[0],
                        'class': course[2],
                        'instructor': course[3],
                        'room_num': course[8],
                        'time': now.strftime("%Y-%m-%d %H:%M:%S")
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