import datetime
import requests

# Get the current year
current_year = datetime.datetime.now().year

# Hard code start dates
start_dates = [datetime.datetime(2024,8,22), #Fall
               datetime.datetime(2025,1,13), #Spring
               datetime.datetime(2025,5,12)] #Summer

end_dates = [datetime.datetime(2024,12,13), #Fall
             datetime.datetime(2025,5,2),   #Spring
             datetime.datetime(2025,8,8)]   #Summer

def check_dates_in_range():
    today = datetime.datetime.now()
    results = []

    for start_date, end_date in zip(start_dates, end_dates):
        if start_date <= today <= end_date:
            results.append(True)
        else:
            results.append(False)

    return results

def after_end_dates():
    today = datetime.datetime.now()
    results = []
    for end_date in end_dates:
        if today > end_date:
            results.append(True)
        else:
            results.append(False)

    return results

# Main logic
def get_term():
    result1 = check_dates_in_range()
    result2 = after_end_dates()
    if result1[0]:
        semester = 8
    elif result1[1]:
        semester = 1
    elif result1[2]:
        semester = 5
    elif not result1[0] and not result1[1] and not result1[2]:
        if result2[2]: # Past Summer go to Fall
            semester = 8
        elif result2[1]: # Past Spring go to Summer
            semester = 5
        elif result2[2]: # Past Fall go to Spring
            semester = 1
        else: # Before Fall
            semester = 8

    modified_year = str(current_year)[0] + str(current_year)[2:]  # Remove the second digit
    return int(modified_year + str(semester))  # Concatenate the modified year with the suffix

def fetch_courses(course_code=None, class_num=None):
    # URL to send the GET request to
    url = "https://one.ufl.edu/apix/soc/schedule/"

    term = get_term()

    # Initialize query parameters
    params = {
        "category": "CWSP",
        "term": term,  # Adjusted to the term you specified 6W1 for A. 6W2 for B. 1 for C
        "last-control-number": 0
    }

    # Add course_code and class_num to params if provided
    if course_code:
        params["course-code"] = course_code
    if class_num:
        params["class-num"] = class_num

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

                # Print the course code and class numbers
                for section in sections:
                    class_number = section.get('classNumber')  # Extract class number
                    #print(f"{i}. {course_code} - {class_number}")
                    course_results.append({
                        "index": i,
                        "course_code": course_code,
                        "class_number": class_number
                    })

            #print(f"retrieved rows: {retrievedrows}")
            #print(f"lastcontrolnumber: {lastcontrolnumber}")
            #print(f"total rows: {totalrows}")
            #print(f"i: {i}")
            params['last-control-number'] = lastcontrolnumber
            start = i + 1

        else:
            print(f"Failed to retrieve data: {response.status_code}")

    return course_results