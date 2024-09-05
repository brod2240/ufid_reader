'''from courseFetch import fetch_courses

# Example usage
course = "COP"  # Example course code (can be None)
#class_num = 17940    # Example class number (can be None)
results = fetch_courses(course_code=course)

codes = [result['course_code'] for result in results]

if codes:
    print("\nRetrieved Courses:")
    for code in codes:
        print(code)
'''

import requests

url = "https://gatorufid.pythonanywhere.com/index"

response = requests.get(url)

    # Check if the request was successful
if response.status_code == 200:
    data = response.text
    print(data)