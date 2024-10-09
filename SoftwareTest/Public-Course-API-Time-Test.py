from datetime import datetime, time
import requests
import time as time_module  # Import time module for measuring duration
import sys

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
    total_meetings = 0
    total_sections = 0
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
                        begin_time_obj = datetime.strptime(meetTimeBegin, "%I:%M %p").time()
                        meetTimeEnd = meetingTime['meetTimeEnd']
                        end_time_obj = datetime.strptime(meetTimeEnd, "%I:%M %p").time()

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
                            #print(meetTimeBegin)
                            #print(meetTimeEnd)
                        # Update the progress indicator for meetings
                        total_meetings += 1
                        sys.stdout.write(f"Sections loaded: {total_sections}")
                        sys.stdout.write("\n")  # Move to next line for sections
                        sys.stdout.write(f"\rMeetings loaded: {total_meetings}")
                        sys.stdout.write("\033[F")

                    # Update the progress indicator for sections
                    total_sections += 1
                        
                    

            params['last-control-number'] = lastcontrolnumber
            start = i + 1

        else:
            print(f"Failed to retrieve data: {response.status_code}")

    return course_results, total_sections, total_meetings

# Define a function to test fetching courses
def test_fetch_courses():
    # Open a file in write mode to save the report
    with open("Public_Course_API_Time_report.txt", "w") as report_file:
        # Days of the week to test
        days = ['M', 'T', 'W', 'R', 'F', 'S', 'U']  # M: Monday, T: Tuesday, W: Wednesday, R: Thursday, F: Friday, S: Saturday, U: Sunday

        # Test each day of the week
        for day in days:
            print(f"Testing for day: {day}")

            start_time = time_module.time()  # Start timing
            results, sections, meetings = fetch_courses(time(11, 0), day, 'NSC215', 
                                                        day_m=('true' if day == 'M' else None), 
                                                        day_t=('true' if day == 'T' else None), 
                                                        day_w=('true' if day == 'W' else None), 
                                                        day_r=('true' if day == 'R' else None), 
                                                        day_f=('true' if day == 'F' else None), 
                                                        day_s=('true' if day == 'S' else None))
            duration = time_module.time() - start_time  # Calculate duration

            # Sections could be higher than meeting due to online classes
            # Prepare messages
            sections_message = f"Sections loaded for {day}: {sections}"
            meetings_message = f"Meetings loaded for {day}: {meetings}"
            results_message = f"Results produced for {day}: {len(results)}"
            time_message = f"Time taken for {day}: {duration:.4f} seconds"

            # Print to console
            print(sections_message)
            print(meetings_message)
            print(results_message)
            print(time_message)

            # Write to the report file
            report_file.write(sections_message + "\n")
            report_file.write(meetings_message + "\n")
            report_file.write(results_message + "\n")
            report_file.write(time_message + "\n")
            report_file.write("\n")  # Add a blank line for readability

        # Final log entry
        print("Loading complete.")
        report_file.write("Loading complete.\n")

if __name__ == '__main__':
    test_fetch_courses()