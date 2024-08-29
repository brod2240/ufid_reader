'''
import requests
import json

# URL to send the GET request to
url = "https://one.ufl.edu/apix/soc/schedule/"

# Query parameters
params = {
    "category": "CWSP",
    "term": "2245"  # Adjusted to the term you specified
}

# Send the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Save JSON data to a file
    #with open('data2.json', 'w') as json_file:
    #    json.dump(data, json_file, indent=4)

    #print("Data saved to data.json")
    print(data)
    
else:
    print(f"Failed to retrieve data: {response.status_code}")

'''



'''
import requests

# URL to send the GET request to
url = "https://one.ufl.edu/apix/soc/schedule/"

# Query parameters
params = {
    "category": "CWSP",
    "term": "2245"  # Adjusted to the term you specified
}

# Send the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Assuming the response contains a dictionary with a 'courses' key
    courses = data[0]['COURSES']  # Use .get() for safe access
    retrievedrows = data[0]['RETRIEVEDROWS']
    
    #course_codes = set()
    # Iterate through each course in the courses list
    for i, course in enumerate(courses, start=1):
       #course_codes.add(course.get('code'))
       course_code = course.get('code')
       sections = course.get('sections', [])

       # Print the course code and class numbers
       for section in sections:
        class_number = section.get('classNumber')  # Extract class number
        print(f"{i}. {course_code} - {class_number}")
    #sorted_course_codes = sorted(course_codes)
    #for i, course_code in enumerate(sorted_course_codes, start=1):
    #    print(f"{i}. {course_code}")
    
        
    print(f"retrieved rows: {retrievedrows}")
    
else:
    print(f"Failed to retrieve data: {response.status_code}")
'''

'''
import requests

# URL to send the GET request to
url = "https://one.ufl.edu/apix/soc/schedule/"

# Query parameters
params = {
    "category": "CWSP",
    "term": "2245",  # Adjusted to the term you specified
    "course-code": ""
}

# Send the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Assuming the response contains a dictionary with a 'courses' key
    courses = data[0]['COURSES']  # Use .get() for safe access
    retrievedrows = data[0]['RETRIEVEDROWS']
    
    course_codes = set()
    # Iterate through each course in the courses list
    for i, course in enumerate(courses, start=1):
       course_codes.add(course.get('code'))
       #course_code = course.get('code')
       #sections = course.get('sections', [])

       # Print the course code and class numbers
       #for section in sections:
        #class_number = section.get('classNumber')  # Extract class number
        #print(f"{i}. {course_code} - {class_number}")
    sorted_course_codes = sorted(course_codes)
    for i, course_code in enumerate(sorted_course_codes, start=1):
        print(f"{i}. {course_code}")
    
        
    print(f"retrieved rows: {retrievedrows}")
    
else:
    print(f"Failed to retrieve data: {response.status_code}")
'''

'''
import requests
import json

def fetch_all_data(url, params, output_file):
    all_data = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Assuming data structure includes 'COURSES', 'RETRIEVEDROWS', 'TOTALROWS', and 'LASTCONTROLNUMBER'
            if len(data) > 0:
                courses = data[0]['COURSES']
                
                # Extract course code and class number
                for course in courses:
                    course_code = course.get('code')
                    sections = course.get('sections', [])
                    for section in sections:
                        class_number = section.get('classNumber')
                        all_data.append({
                            "course_code": course_code,
                            "class_number": class_number
                        })
                
                retrieved_rows = data[0]['RETRIEVEDROWS']
                total_rows = data[0]['TOTALROWS']
                last_control_number = data[0]['LASTCONTROLNUMBER']
                
                print(f"Retrieved Rows: {retrieved_rows}")
                print(f"Total Rows: {total_rows}")
                print(f"Last Control Number: {last_control_number}")

                # Check if we have retrieved all data
                if len(all_data) >= total_rows:
                    break

                # Update parameters for the next page if pagination is supported
                params['last-control-number'] = last_control_number  # Adjust based on API documentation
            else:
                break
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            break

    # Save collected data to a JSON file with each row as a separate JSON object
    numbered_data = [{"index": i + 1, "course_code": entry["course_code"], "class_number": entry["class_number"]} for i, entry in enumerate(all_data)]
    with open(output_file, 'w') as json_file:
        json.dump(numbered_data, json_file, indent=4)

    print(f"Data saved to {output_file}")

# Example usage
url = "https://one.ufl.edu/apix/soc/schedule/"
params = {
    "category": "CWSP",
    "term": "2245",
    "last-control-number": 0  # Initial parameter to start fetching data
}
output_file = 'course_codes_and_class_numbers.json'

fetch_all_data(url, params, output_file)
'''



'''
import requests
import json

# URL to send the GET request to
url = "https://one.ufl.edu/apix/soc/schedule/"

# Query parameters
params = {
    "category": "CWSP",
    "term": "2245",
    "last-control-number": 0  # Initial parameter to start fetching data
}

all_courses = []  # List to hold all course data

while True:
    # Send the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Assuming the response contains a dictionary with a 'courses' key
        courses_data = data[0]
        courses = courses_data['COURSES']  # Use .get() for safe access
        retrievedrows = courses_data['RETRIEVEDROWS']
        totalrows = courses_data['TOTALROWS']
        last_control_number = courses_data['LASTCONTROLNUMBER']

        # Append current batch of courses to the all_courses list
        for course in courses:
            course_code = course.get('code')
            sections = course.get('sections', [])
            for section in sections:
                class_number = section.get('classNumber')
                all_courses.append({
                    "course_code": course_code,
                    "class_number": class_number
                })

        # Check if we have retrieved all rows
        if len(all_courses) >= totalrows:
            break

        # Update the 'start' parameter to fetch the next set of results
        params['last-control-number'] = last_control_number

    else:
        print(f"Failed to retrieve data: {response.status_code}")
        break

# Number the courses starting from 1
numbered_courses = [{"index": i + 1, "course_code": entry["course_code"], "class_number": entry["class_number"]} for i, entry in enumerate(all_courses)]

# Save to JSON file
output_file = 'course_codes_and_class_numbers.json'
with open(output_file, 'w') as json_file:
    json.dump(numbered_courses, json_file, indent=4)

print(f"Data saved to {output_file}")
print(f"Total retrieved rows: {len(all_courses)}")
'''
##USE THIS
'''
import requests
from HTMLparser import main
import json

# URL to send the GET request to
url = "https://one.ufl.edu/apix/soc/schedule/"

term = main()

def fetch_courses(course_code=None, class_num=None):
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
            totalrows = data[0]['TOTALROWS']

            if retrievedrows == 0 and lastcontrolnumber == 0:
                break
            
            # Iterate through each course in the courses list
            for i, course in enumerate(courses, start):
                course_code = course.get('code')
                sections = course.get('sections', [])

                # Print the course code and class numbers
                for section in sections:
                    class_number = section.get('classNumber')  # Extract class number
                    print(f"{i}. {course_code} - {class_number}")
                    course_results.append({
                        "index": i,
                        "course_code": course_code,
                        "class_number": class_number
                    })

            print(f"retrieved rows: {retrievedrows}")
            print(f"lastcontrolnumber: {lastcontrolnumber}")
            print(f"total rows: {totalrows}")
            print(f"i: {i}")
            params['last-control-number'] = lastcontrolnumber
            start = i + 1
            
        else:
            print(f"Failed to retrieve data: {response.status_code}")

    return course_results

# Example usage
course_code = "COP"  # Example course code (can be None)
#class_num = 17940    # Example class number (can be None)
results = fetch_courses(course_code)

# Print out the results
if results:
    print("\nRetrieved Courses:")
    for result in results:
        print(f"Index: {result['index']}, Course Code: {result['course_code']}, Class Number: {result['class_number']}")
else:
    print("No courses retrieved.")

'''
#TEST
import requests
from HTMLparser import main
import json

# URL to send the GET request to
url = "https://one.ufl.edu/apix/soc/schedule/"

term = main()

# Query parameters
params = {
    "category": "CWSP",
    "term": term,  # Adjusted to the term you specified 6W1 for A. 6W2 for B. 1 for C
    "last-control-number": 0,
    #"course-code": "COP"
    "class-num": 17940
}

course_results = []
start = 1
done = 0
while True: 
    # Send the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        print(data)
        
    else:
        print(f"Failed to retrieve data: {response.status_code}")
